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

logging.basicConfig(level=logging.INFO)


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
            header = struct.unpack("<hhhHHLllhh", chunk)

            is_deflated = header[2] == 8
            crc_32 = header[5]
            compressed_size = header[6]
            decompressed_size = header[7]
            filename_len = header[8]
            extra_len = header[9]

            filename = f.read(filename_len)
            if extra_len > 0:
                f.read(extra_len)

            os.makedirs(os.path.dirname(filename), exist_ok=True)

            if dry_run:
                print(f"{decompressed_size:10d} {filename.decode('ascii'):s}")
                continue

            if compressed_size == 0:
                continue

            contents = f.read(compressed_size)
            if len(contents) < compressed_size:
                logging.warn(f"{filename} is truncated")

            if is_deflated:
                try:
                    contents = zlib.decompress(
                        contents, wbits=-zlib.MAX_WBITS, bufsize=decompressed_size
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
