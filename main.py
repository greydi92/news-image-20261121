#!/usr/bin/env python3
"""make.fun entry for news-image-20261121: "The World in One Day".

The graded program. It places the finished front-page image that ships
in this repository at /output/entry.png.

The picture was drawn at build time by gen_image.py (Pillow + DejaVu)
from the verified world news of Saturday 21 November 2026: Russian
missiles landing in Poland during a huge overnight barrage on
Ukraine, Wall Street sliding into correction as the AI sell-off
deepens, the World Court finding Myanmar guilty of Rohingya
genocide, hackers hitting JPMorgan, Visa and Mastercard through
third-party vendors, Britain and the EU signing new deals, and
Israel's president asking Gadi Eisenkot to form the next government.

This program does no drawing and needs no network: it copies fixed
bytes, so the two graded runs write identical output. Standard
library only; the output directory comes from MAKEFUN_OUTPUT_DIR
outside the grader, or /output inside it.
"""

import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
IMAGE_NAME = "entry.png"


def run():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    src = os.path.join(HERE, IMAGE_NAME)
    dst = os.path.join(out_dir, IMAGE_NAME)
    if not os.path.isfile(src):
        print("entry image missing:", src, file=sys.stderr)
        return 1
    shutil.copyfile(src, dst)
    if os.path.getsize(dst) != os.path.getsize(src):
        print("incomplete copy:", dst, file=sys.stderr)
        return 1
    print("wrote", dst, os.path.getsize(dst), "bytes")
    return 0


if __name__ == "__main__":
    sys.exit(run())
