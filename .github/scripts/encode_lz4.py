#!/usr/bin/env python3
"""Encode CPIO into legacy LZ4 block format (0x02 0x21 0x4C 0x18 header).

v3.1 fix: Added input size sanity check to prevent silent corruption
if the CPIO exceeds 64MB (partition limit).
"""
import sys, lz4.block

infile, outfile = sys.argv[1], sys.argv[2]
MAX_INPUT = 64 * 1024 * 1024  # 64 MB partition limit

with open(infile, 'rb') as f:
    data = f.read()

if len(data) > MAX_INPUT:
    print(f"ERROR: Input {len(data):,} bytes exceeds 64MB partition limit", file=sys.stderr)
    sys.exit(1)

output = bytearray(b'\x02\x21\x4c\x18')  # LZ4 legacy header
BLOCK = 8 * 1024 * 1024

for i in range(0, len(data), BLOCK):
    blk = data[i:i + BLOCK]
    comp = lz4.block.compress(blk, mode='high_compression', compression=12, store_size=False)
    output += len(comp).to_bytes(4, 'little') + comp

with open(outfile, 'wb') as f:
    f.write(output)
print(f"LZ4: {len(output):,} bytes ({len(output)/1024/1024:.2f} MB)")