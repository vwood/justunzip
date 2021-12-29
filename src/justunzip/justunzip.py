#!/usr/bin/env python3

"""
CLI script to unzip truncated or corrupt zip files
"""

import struct
import os
import sys
import zlib
import logging
import click
from dataclasses import dataclass

logging.basicConfig(level=logging.INFO)


@dataclass
class ZipLocalFileHeader:
    version: int
    bitflag: int
    compression_method: int
    modification_time: int
    modification_date: int
    crc32: int
    compressed_size: int
    uncompressed_size: int
    filename_length: int
    extra_field_length: int


def decompress(archive_filename, dry_run):
    """
    Decompress `filename` into current directory.
    """
    with open(archive_filename, "rb") as f:
        print(f"Archive: {archive_filename}")

        if dry_run:
            print(f"{'Length':10s} Name")
            print(f"{'-'*10} {'-'*4}")

        while chunk := f.read(4):
            if len(chunk) < 4:
                break

            if chunk != b"PK\x03\x04":
                f.seek(-3, 1)
                continue

            logging.debug(f"found header @ 0x{f.tell() - 4:x}")

            chunk = f.read(2 + 2 + 2 + 2 + 2 + 4 + 4 + 4 + 2 + 2)
            header = ZipLocalFileHeader(*struct.unpack("<hhhHHLllhh", chunk))

            is_deflated = header.compression_method == 8

            filename = f.read(header.filename_length)
            if header.extra_field_length > 0:
                f.read(header.extra_field_length)

            if dry_run:
                print(f"{header.uncompressed_size:10d} {filename.decode('ascii'):s}")
                continue

            dirname = os.path.dirname(filename)
            if len(dirname) > 0:
                os.makedirs(dirname, exist_ok=True)

            if header.compressed_size == 0:
                continue

            contents = f.read(header.compressed_size)
            if len(contents) < header.compressed_size:
                logging.warn(f"{filename} is truncated")

            if is_deflated:
                try:
                    contents = zlib.decompress(
                        contents,
                        wbits=-zlib.MAX_WBITS,
                        bufsize=header.uncompressed_size,
                    )
                except zlib.error as e:
                    logging.error(f"error decompressing {filename}")

            print(f"creating: {filename.decode('ascii'):s}")
            with open(filename, "wb") as new_file:
                new_file.write(contents)


@click.command()
@click.option("-l", "--dry_run", is_flag=True, default=False)
@click.argument("filenames", nargs=-1, required=True)
def main(filenames, dry_run):
    for filename in filenames:
        try:
            decompress(filename, dry_run)
        except Exception as ex:
            logging.exception(f"Error with file: '{filename}'")
