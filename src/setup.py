import os
import sys
from typing import List

from setuptools import find_namespace_packages, setup

sys.path.append(os.path.join(os.path.dirname(__file__), "src"))

CURRENT_PYTHON = sys.version_info[:2]
REQUIRED_PYTHON = (3, 11)
EGG_NAME = "micropython_mdns"


def list_packages(source_directory: str = ".") -> List[str]:
    packages = list(find_namespace_packages(source_directory, exclude="venv"))
    return packages


__version__ = "1.8.0"
requirements = []
test_requirements = ["twine", "adafruit-ampy>=1.0.0"]

readme_location = "README.md"
if os.path.isfile(readme_location):
    with open(readme_location, "r") as handle:
        long_description = handle.read()
else:
    long_description = ""


setup(
    name=EGG_NAME,
    version=__version__,
    python_requires=">={}.{}".format(*REQUIRED_PYTHON),
    url="https://github.com/cbrand/micropython-mdns",
    author="Christoph Brand",
    author_email="ch.brand@gmail.com",
    description="MDNS for micropython with service discovery support",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="MIT",
    packages=list_packages(),
    include_package_data=True,
    install_requires=requirements,
    zip_safe=True,
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: Implementation :: MicroPython",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "Programming Language :: Python :: 3 :: Only",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: System :: Networking",
        "License :: OSI Approved :: MIT License",
    ],
    extras_require={},
    project_urls={"GitHub": "https://github.com/cbrand/micropython-mdns"},
)
