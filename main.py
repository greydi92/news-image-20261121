#!/usr/bin/env python3
"""Entry point for the news-image-20261121 competition.

Copies the pre-rendered front-page image (entry.png, shipped in this
repository) into the grader's output directory. Standard library only,
no network, fully deterministic: the same bytes go out every run.
"""

import os
import shutil
import sys

IMAGE_NAME = "entry.png"


def locate_source():
    """Path of the image sitting next to this file."""
    here = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(here, IMAGE_NAME)


def locate_target_dir():
    """Grader output dir: MAKEFUN_OUTPUT_DIR, else /output."""
    chosen = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    return chosen


def run():
    source = locate_source()
    if not os.path.isfile(source):
        print("missing image: " + source, file=sys.stderr)
        return 1
    target_dir = locate_target_dir()
    os.makedirs(target_dir, exist_ok=True)
    target = os.path.join(target_dir, IMAGE_NAME)
    shutil.copyfile(source, target)
    if os.path.getsize(target) != os.path.getsize(source):
        print("copy size mismatch: " + target, file=sys.stderr)
        return 1
    print("copied " + source + " -> " + target)
    return 0


if __name__ == "__main__":
    sys.exit(run())
