#!/usr/bin/env python3
"""Decode legacy LZ4 block format (0x02 0x21 0x4C 0x18 header) to CPIO.

v3.2 fix: Improved error handling, configurable max uncompressed size.
"""
import sys
import lz4.block

def decode_lz4(infile, outfile, max_uncompressed=64 * 1024 * 1024):
    """Decode LZ4 block format to CPIO."""
    with open(infile, 'rb') as f:
        data = f.read()

    if len(data) < 4:
        raise ValueError(f"File too small: {len(data)} bytes")

    # Check magic header
    magic = data[:4]
    expected = b'\x02\x21\x4c\x18'
    if magic != expected:
        raise ValueError(f"Invalid LZ4 header: {magic.hex()} (expected {expected.hex()})")

    pos = 4
    output = bytearray()
    block_count = 0

    while pos < len(data):
        if pos + 4 > len(data):
            raise ValueError(f"Truncated block size at position {pos}")

        bs = int.from_bytes(data[pos:pos+4], 'little')
        pos += 4

        if bs == 0:
            break  # End marker

        if pos + bs > len(data):
            raise ValueError(f"Block {block_count}: truncated data (need {bs}, have {len(data)-pos})")

        block_data = data[pos:pos+bs]
        pos += bs

        try:
            decompressed = lz4.block.decompress(block_data, uncompressed_size=max_uncompressed)
        except Exception as e:
            raise ValueError(f"Block {block_count}: decompression failed: {e}")

        output += decompressed
        block_count += 1

        if len(output) > max_uncompressed:
            raise ValueError(f"Decompressed size {len(output)} exceeds limit {max_uncompressed}")

    with open(outfile, 'wb') as f:
        f.write(output)

    print(f"Decoded: {len(output):,} bytes ({block_count} blocks) -> {outfile}")
    return len(output)


if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("Usage: decode_lz4.py <input.lz4> <output.cpio> [max_uncompressed_mb]")
        sys.exit(1)

    infile, outfile = sys.argv[1], sys.argv[2]
    max_mb = int(sys.argv[3]) if len(sys.argv) > 3 else 64

    try:
        decode_lz4(infile, outfile, max_mb * 1024 * 1024)
    except Exception as e:
        print(f"ERROR: {e}", file=sys.stderr)
        sys.exit(1)