#!/usr/bin/env python3
import sys, lz4.block
infile, outfile = sys.argv[1], sys.argv[2]
with open(infile, 'rb') as f:
    data = f.read()
pos = 4
output = bytearray()
while pos < len(data):
    if pos + 4 > len(data): break
    bs = int.from_bytes(data[pos:pos+4], 'little')
    pos += 4
    if bs == 0: break
    output += lz4.block.decompress(data[pos:pos+bs], uncompressed_size=16*1024*1024)
    pos += bs
with open(outfile, 'wb') as f:
    f.write(output)
print(f"Decoded: {len(output):,} bytes -> {outfile}")
