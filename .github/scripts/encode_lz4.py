#!/usr/bin/env python3
"""Encode CPIO into legacy LZ4 block format (0x02 0x21 0x4C 0x18 header).

v3.2: Improved error handling, configurable block size, high compression.
"""
import sys
import lz4.block

def encode_lz4(infile, outfile, block_size=8 * 1024 * 1024, max_input=128 * 1024 * 1024, compression=12):
    """Encode CPIO to LZ4 block format."""
    with open(infile, 'rb') as f:
        data = f.read()

    if len(data) == 0:
        raise ValueError("Input file is empty")

    if len(data) > max_input:
        raise ValueError(f"Input {len(data):,} bytes exceeds {max_input:,} bytes limit")

    output = bytearray(b'\x02\x21\x4c\x18')  # LZ4 legacy header
    block_count = 0

    for i in range(0, len(data), block_size):
        blk = data[i:i + block_size]
        comp = lz4.block.compress(blk, mode='high_compression', compression=compression, store_size=False)
        
        if len(comp) >= len(blk):
            # Compression didn't help, store uncompressed (but still wrapped)
            pass  # lz4.block handles this
        
        output += len(comp).to_bytes(4, 'little') + comp
        block_count += 1

    # End marker
    output += b'\x00\x00\x00\x00'

    with open(outfile, 'wb') as f:
        f.write(output)

    ratio = len(data) / len(output) if len(output) > 0 else 0
    print(f"Encoded: {len(data):,} -> {len(output):,} bytes ({block_count} blocks, ratio: {ratio:.2f}) -> {outfile}")
    return len(output)


if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("Usage: encode_lz4.py <input.cpio> <output.lz4> [block_size_mb] [max_input_mb] [compression_level]")
        sys.exit(1)

    infile, outfile = sys.argv[1], sys.argv[2]
    block_mb = int(sys.argv[3]) if len(sys.argv) > 3 else 8
    max_mb = int(sys.argv[4]) if len(sys.argv) > 4 else 128
    compression = int(sys.argv[5]) if len(sys.argv) > 5 else 12

    try:
        encode_lz4(infile, outfile, block_mb * 1024 * 1024, max_mb * 1024 * 1024, compression)
    except Exception as e:
        print(f"ERROR: {e}", file=sys.stderr)
        sys.exit(1)