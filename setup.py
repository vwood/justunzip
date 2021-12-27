#!/usr/bin/env python

import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="justunzip",
    version="0.0.1",
    author="vwood",
    author_email="vwood@vwood.org",
    description="unzip truncated or corrupt zip files",
    long_description=long_description,
    long_description_content_type="text/markdown",
    entry_points = {
        'console_scripts': ['justunzip=justunzip.justunzip:main'],
        },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    install_requires=[
        'click>=7.1',
    ],
    python_requires=">=3.6",
)