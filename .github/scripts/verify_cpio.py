#!/usr/bin/env python3
"""Verify CPIO integrity inside LZ4 block file.

v3.1 fix: uncompressed_size increased to 64MB to match TEE ramdisk size.
"""
import sys, lz4.block

lz4file = sys.argv[1]
MAX_UNCOMPRESSED = 64 * 1024 * 1024  # 64 MB

with open(lz4file, 'rb') as f:
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

with open('/tmp/verify.cpio', 'wb') as f:
    f.write(output)
print(f"Decoded: {len(output):,} bytes")

