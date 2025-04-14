#!/usr/bin/env python3

from __future__ import annotations

import argparse
import re

from dunamai import Style, Version

version1_regex = re.compile(r"^version[\s]*=")
version2_regex = re.compile(r"^VERSION[\s]*=")


def update_version_in_file(file: str, version: str):
    with open(file) as f:
        c = f.read()

    lines = []
    for line in c.splitlines():
        if version1_regex.match(line):
            lines.append(f'version = "{version}"')
        elif version2_regex.match(line):
            lines.append(f'VERSION = "{version}"')
        else:
            lines.append(line)

    with open(file, "w") as g:
        g.write("\n".join(lines))


def update_version(files: list[str], force_version: str | None = None):
    if force_version is None:
        version = Version.from_git().serialize(style=Style.SemVer)
    else:
        version = force_version

    for file in files:
        update_version_in_file(file, version)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Update version strings in files. By default, extracts version from git."
    )
    parser.add_argument(
        "--force-version",
        help="Force a specific version instead of auto-detecting from git",
    )
    parser.add_argument("files", nargs="+", help="Files to update version in")
    args = parser.parse_args()

    update_version(args.files, args.force_version)
