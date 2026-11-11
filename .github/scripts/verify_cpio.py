#!/usr/bin/env python3
"""Verify CPIO integrity inside LZ4 block file.

v3.2: Improved error handling, configurable max uncompressed size, returns decoded path.
"""
import sys
import lz4.block

def verify_lz4(lz4file, max_uncompressed=64 * 1024 * 1024, output_path='/tmp/verify.cpio'):
    """Verify and extract LZ4 block format to CPIO."""
    with open(lz4file, 'rb') as f:
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

    # Verify CPIO magic
    if len(output) < 6:
        raise ValueError("Decompressed data too small for CPIO")

    cpio_magic = output[:6]
    if cpio_magic != b'070701':
        raise ValueError(f"Invalid CPIO magic: {cpio_magic} (expected 070701)")

    with open(output_path, 'wb') as f:
        f.write(output)

    print(f"Verified: {len(output):,} bytes ({block_count} blocks), CPIO magic OK -> {output_path}")
    return output_path


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: verify_cpio.py <input.lz4> [max_uncompressed_mb] [output_path]")
        sys.exit(1)

    lz4file = sys.argv[1]
    max_mb = int(sys.argv[2]) if len(sys.argv) > 2 else 64
    output_path = sys.argv[3] if len(sys.argv) > 3 else '/tmp/verify.cpio'

    try:
        verify_lz4(lz4file, max_mb * 1024 * 1024, output_path)
    except Exception as e:
        print(f"ERROR: {e}", file=sys.stderr)
        sys.exit(1)