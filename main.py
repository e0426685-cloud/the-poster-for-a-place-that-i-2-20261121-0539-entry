#!/usr/bin/env python3
"""LUMARA — travel poster for a place that isn't there.

Entry program for make.fun's "The Poster for a Place That Isn't
There". It writes one image to /output/entry.png: the poster for
LUMARA, the City of Two Dawns, a cliffside harbour city under twin
suns with a spiral lighthouse.

The poster image is prebuilt (see build_poster.py, which drew it
with Pillow at build time). This program uses only the Python
standard library, so it runs in the grader's sandbox with no
network and no third-party packages: it simply copies the finished
poster to /output/entry.png.
"""

import shutil
from pathlib import Path

HERE = Path(__file__).resolve().parent
SRC = HERE / "poster.png"
DST = Path("/output/entry.png")


def main() -> None:
    DST.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(SRC, DST)


if __name__ == "__main__":
    main()
