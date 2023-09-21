#!/usr/bin/python3

import json
import re
from os import walk
from pathlib import Path
from typing import TypedDict


VERSION_FINDER = re.compile(
    r'__version__\s*=\s*"(?P<version>[0-9]+\.[0-9]+\.[0-9]+)"', re.MULTILINE | re.UNICODE | re.IGNORECASE
)


class MipDict(TypedDict):
    version: str
    deps: list[str]
    urls: list[list[str]]


def get_root_path() -> Path:
    return Path(__file__, "..", "src").resolve()


def get_package_json_path() -> Path:
    return (get_root_path() / ".." / "package.json").resolve()


def get_setup_py_path() -> Path:
    return get_root_path() / "setup.py"


def generate_urls_entries() -> list[list[str]]:
    urls = []
    root_path = get_root_path()
    for root, _, files in walk(root_path / "mdns_client"):
        for file in files:
            file_path = Path(root, file)
            if file_path.suffix == ".py":
                relpath = str(file_path.relative_to(root_path)).replace("\\", "/")
                urls.append([relpath, f"github:cbrand/micropython-mdns/src/{relpath}"])
    return urls


def get_current_version() -> str:
    for item in get_setup_py_path().read_text().split("\n"):
        matcher = VERSION_FINDER.match(item)
        if matcher is not None:
            return matcher.group("version")
    return "dev"


def generate_mip_json() -> MipDict:
    return MipDict(
        version=get_current_version(),
        deps=[],
        urls=generate_urls_entries(),
    )


if __name__ == "__main__":
    package_json_path = get_package_json_path()
    package_json_path.write_text(json.dumps(generate_mip_json()))
