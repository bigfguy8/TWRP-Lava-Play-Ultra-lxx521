#!/usr/bin/env python3
"""Decode legacy LZ4 block format (0x02 0x21 0x4C 0x18 header) to CPIO.

v3.1 fix: uncompressed_size increased from 16MB to 64MB to handle
TEE-injected ramdisks that may exceed the original 16MB limit.
"""
import sys, lz4.block

infile, outfile = sys.argv[1], sys.argv[2]
MAX_UNCOMPRESSED = 64 * 1024 * 1024  # 64 MB

with open(infile, 'rb') as f:
    data = f.read()

pos = 4
output = bytearray()
while pos < len(data):
    if pos + 4 > len(data):
        break
    bs = int.from_bytes(data[pos:pos+4], 'little')
    pos += 4
    if bs == 0:
        break
    output += lz4.block.decompress(data[pos:pos+bs], uncompressed_size=MAX_UNCOMPRESSED)
    pos += bs

with open(outfile, 'wb') as f:
    f.write(output)
print(f"Decoded: {len(output):,} bytes -> {outfile}")