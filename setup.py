#!/usr/bin/env python

import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

VERSION="0.0.11"

setuptools.setup(
    name="justunzip",
    version=VERSION,
    license="MIT",
    author="vwood",
    author_email="vwood@vwood.org",
    description="unzip truncated or corrupt zip files",
    long_description=long_description,
    long_description_content_type="text/markdown",
    entry_points={
        "console_scripts": ["justunzip=justunzip.justunzip:main"],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Environment :: Console",
        "Topic :: System :: Archiving :: Compression",
        "Topic :: Utilities",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    install_requires=[
        "click>=7.1",
    ],
    python_requires=">=3.6",
    download_url=f"https://github.com/vwood/justunzip/archive/refs/tags/v{VERSION}.tar.gz",
    url="https://github.com/vwood/justunzip",
    keywords="zip truncated corrupt zipfile archive unzip",
)
