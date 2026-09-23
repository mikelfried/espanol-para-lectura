#!/usr/bin/env python3
"""Screenshot a local HTML file with headless Chrome at a given size.

Uses build.run_chrome, which waits for the output file and then kills Chrome,
because Chrome writes the file and then does not reliably exit.
"""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).parent.parent))
import build  # noqa: E402


def shot(src, out, w, h, scale=1, extra=()):
    out = pathlib.Path(out).resolve()
    if out.exists():
        out.unlink()
    build.run_chrome([f"--window-size={w},{h}", f"--force-device-scale-factor={scale}",
                      "--hide-scrollbars", *extra, f"--screenshot={out}",
                      pathlib.Path(src).resolve().as_uri()],
                     wait_for=out, profile="shot")
    return out.exists()


if __name__ == "__main__":
    src, out, w, h = sys.argv[1:5]
    scale = float(sys.argv[5]) if len(sys.argv) > 5 else 1
    print(out, "ok" if shot(src, out, int(w), int(h), scale) else "FAILED")
