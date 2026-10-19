"""Capture the SVG header offline and encode a looping WebP for README images."""

import argparse
from functools import partial
from hashlib import sha256
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
import json
from pathlib import Path
import re
import shutil
import subprocess
import tempfile
import threading

from build_profile_header import render

ROOT = Path(__file__).resolve().parents[1]
SECONDS = 16
CAPTURE_FPS = 30
VARIANTS = ("dark", "light", "mobile-dark", "mobile-light")


def loop_markup(theme, mobile):
    # All motions must meet at the same pose when the encoded loop restarts.
    # Preserve each droplet's initial phase while sharing a 16-second period.
    markup = render(theme, mobile)
    for before, after in (("12s", "16s"), ("10s", "16s"),
                          ("14s", "16s"), ('dur="32s"', 'dur="16s"'),
                          ("-4s", "-5.333333333s"), ("-3s", "-4.8s")):
        markup = markup.replace(before, after)
    return markup


def publish(manifest, output):
    """Preflight every asset and responsive reference before changing README."""
    if set(manifest) != set(VARIANTS):
        raise ValueError("All four variants are required before publishing")
    readme = (ROOT / "README.md").read_text()
    assets = []
    for variant, metadata in manifest.items():
        source = output / metadata["file"]
        data = source.read_bytes()
        digest = sha256(data).hexdigest()
        if digest != metadata["sha256"] or len(data) != metadata["bytes"]:
            raise ValueError(f"Asset changed after validation: {variant}")
        if not (data.startswith(b"RIFF") and data[8:12] == b"WEBP"):
            raise ValueError(f"Invalid WebP: {variant}")
        if len(data) > 3 * 1024 * 1024:
            raise ValueError(f"WebP exceeds the 3 MiB publication budget: {variant}")
        filename = f"header-{variant}-{digest[:12]}.webp"
        pattern = rf"assets/header-{variant}-[a-f0-9]{{12}}\.(?:svg|webp)"
        readme, count = re.subn(pattern, "assets/" + filename, readme)
        if count != 1:
            raise ValueError(f"Expected one animated README source: {variant}")
        assets.append((source, ROOT / "assets" / filename))
    for source, target in assets:
        shutil.copyfile(source, target)
    (ROOT / "README.md").write_text(readme)
    for path in (ROOT / "assets").glob("header-*.webp"):
        if path not in [target for _, target in assets]:
            path.unlink()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--variants", nargs="+", choices=VARIANTS, default=list(VARIANTS))
    parser.add_argument("--fps", type=int, default=24)
    parser.add_argument("--scale", type=float, default=1.5)
    parser.add_argument("--quality", type=int, default=88)
    parser.add_argument("--lossless", action="store_true")
    parser.add_argument("--output", type=Path, default=ROOT / "output/prerender")
    parser.add_argument("--publish", action="store_true", help="Copy all four variants into assets and update README")
    args = parser.parse_args()
    if not 10 <= args.fps <= CAPTURE_FPS or not 1 <= args.scale <= 2 or not 0 <= args.quality <= 100:
        parser.error("fps must be 10–30, scale 1–2, and quality 0–100")
    if args.publish and set(args.variants) != set(VARIANTS):
        parser.error("publishing requires all four responsive/theme variants")
    for command in ("npx", "ffmpeg", "chromium"):
        if not shutil.which(command):
            parser.error(f"missing build dependency: {command}")
    output = args.output.resolve()
    output.mkdir(parents=True, exist_ok=True)
    cli = ["npx", "--yes", "--package", "@playwright/cli", "playwright-cli",
           "--session", "header-prerender"]

    def browser(*command):
        result = subprocess.run([*cli, *command], cwd=ROOT, text=True,
                                stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        if result.returncode or "### Error" in result.stdout:
            raise RuntimeError(result.stdout)
        return result.stdout

    manifest = {}
    with tempfile.TemporaryDirectory(prefix="profile-prerender-") as temporary:
        work = Path(temporary)
        config = work / "browser.json"
        config.write_text(json.dumps({"browser": {
            "browserName": "chromium",
            "launchOptions": {"executablePath": shutil.which("chromium"), "headless": True},
            "contextOptions": {"deviceScaleFactor": args.scale, "colorScheme": "dark",
                               "reducedMotion": "no-preference"},
        }}))
        handler = partial(SimpleHTTPRequestHandler, directory=str(work))
        server = ThreadingHTTPServer(("127.0.0.1", 0), handler)
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        address = f"http://127.0.0.1:{server.server_port}"
        try:
            browser("open", "about:blank", "--config", str(config))
            for variant in args.variants:
                mobile = variant.startswith("mobile-")
                theme = variant.removeprefix("mobile-")
                width, height = (400, 690) if mobile else (960, 370)
                frames = output / variant
                frames.mkdir(exist_ok=True)
                markup = loop_markup(theme, mobile)
                signature = {"source": sha256(markup.encode()).hexdigest(), "scale": args.scale,
                             "frames": SECONDS * CAPTURE_FPS}
                stamp = frames / "capture.json"
                reusable = (stamp.exists() and json.loads(stamp.read_text()) == signature
                            and all((frames / f"frame-{i:04d}.png").is_file()
                                    for i in range(SECONDS * CAPTURE_FPS)))
                (work / "header.html").write_text(
                    '<!doctype html><meta charset="utf-8"><style>html,body{margin:0;padding:0}</style>' + markup)
                setup = f'''async(page)=>{{
                  await page.setViewportSize({{width:{width},height:{height}}});
                  await page.goto({json.dumps(address + '/header.html')},{{waitUntil:'load'}});
                  await page.evaluate(async()=>{{
                    await document.fonts.ready;
                    await Promise.all([...document.querySelectorAll('image')].map(async el=>{{
                      const image=new Image();image.src=el.href.baseVal;await image.decode();
                    }}));
                    window.captureAnimations=document.getAnimations();
                    window.captureAnimations.forEach(a=>a.pause());
                    document.querySelectorAll('svg').forEach(s=>s.pauseAnimations());
                  }});
                }}'''
                if not reusable:
                    browser("run-code", setup)
                for start in (() if reusable else range(0, SECONDS * CAPTURE_FPS, 60)):
                    end = min(start + 60, SECONDS * CAPTURE_FPS)
                    capture = f'''async(page)=>{{
                      for(let frame={start};frame<{end};frame++){{
                        await page.evaluate(t=>{{
                          document.querySelectorAll('svg').forEach(s=>s.setCurrentTime(t));
                          window.captureAnimations.forEach(a=>a.currentTime=t*1000);
                        }},frame/{CAPTURE_FPS});
                        await page.screenshot({{path:{json.dumps(str(frames))}+'/frame-'+String(frame).padStart(4,'0')+'.png'}});
                      }}
                      return {{captured:{end}}};
                    }}'''
                    browser("run-code", capture)
                    print(f"{variant}: {end}/{SECONDS * CAPTURE_FPS} frames", flush=True)
                stamp.write_text(json.dumps(signature))
                destination = output / f"header-{variant}.webp"
                # Keep enough resolution for the profile's actual display size,
                # rather than encoding every high-density capture pixel.
                encoded_width = 600 if mobile else 1152
                encoded_height = 1035 if mobile else 444
                subprocess.run([
                    "ffmpeg", "-hide_banner", "-loglevel", "error", "-y",
                    "-framerate", str(CAPTURE_FPS), "-i", str(frames / "frame-%04d.png"),
                    "-vf", f"fps={args.fps},scale={encoded_width}:{encoded_height}:flags=lanczos",
                    "-frames:v", str(SECONDS * args.fps), "-c:v", "libwebp_anim",
                    "-lossless", str(int(args.lossless)), "-quality", str(args.quality),
                    "-compression_level", "4", "-loop", "0",
                    str(destination),
                ], check=True)
                manifest[variant] = {"file": destination.name, "bytes": destination.stat().st_size,
                                     "sha256": sha256(destination.read_bytes()).hexdigest(),
                                     "fps": args.fps, "seconds": SECONDS,
                                     "encoded_width": encoded_width, "encoded_height": encoded_height,
                                     "quality": args.quality, "lossless": args.lossless,
                                     "display_width": width, "display_height": height}
                print(f"{variant}: {destination.stat().st_size:,} bytes", flush=True)
                (output / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
        finally:
            browser("close")
            server.shutdown()
            server.server_close()
    (output / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    if args.publish:
        publish(manifest, output)


if __name__ == "__main__":
    main()
