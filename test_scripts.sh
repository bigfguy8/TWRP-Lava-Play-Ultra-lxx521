#!/usr/bin/env bash
# Local test script for TWRP build utilities
# Run this to verify the Python scripts work correctly

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TEST_DIR="/tmp/twrp_test_$$"

cleanup() {
    rm -rf "$TEST_DIR"
}
trap cleanup EXIT

mkdir -p "$TEST_DIR"

echo "=== Testing LZ4 encode/decode/verify scripts ==="

# Create test CPIO data
echo "Creating test CPIO..."
cd "$TEST_DIR"
mkdir -p test_root/{bin,lib,etc}
echo "#!/bin/sh" > test_root/init
echo "echo hello" >> test_root/init
chmod +x test_root/init
echo "test file" > test_root/etc/test.conf
dd if=/dev/urandom of=test_root/lib/bigfile bs=1M count=10 2>/dev/null

# Create CPIO
cd test_root
find . | cpio -o -H newc --owner=0:0 > ../test.cpio
cd ..
echo "CPIO size: $(stat -c%s test.cpio) bytes"

# Test encode_lz4.py
echo ""
echo "--- Testing encode_lz4.py ---"
python3 "$SCRIPT_DIR/.github/scripts/encode_lz4.py" test.cpio test.lz4
echo "LZ4 size: $(stat -c%s test.lz4) bytes"

# Test decode_lz4.py
echo ""
echo "--- Testing decode_lz4.py ---"
python3 "$SCRIPT_DIR/.github/scripts/decode_lz4.py" test.lz4 test_decoded.cpio
echo "Decoded CPIO size: $(stat -c%s test_decoded.cpio) bytes"

# Test verify_cpio.py
echo ""
echo "--- Testing verify_cpio.py ---"
python3 "$SCRIPT_DIR/.github/scripts/verify_cpio.py" test.lz4 64 /tmp/verify_test.cpio
echo "Verified CPIO size: $(stat -c%s /tmp/verify_test.cpio) bytes"

# Verify round-trip
echo ""
echo "--- Verifying round-trip integrity ---"
if cmp -s test.cpio test_decoded.cpio; then
    echo "✓ encode -> decode: IDENTICAL"
else
    echo "✗ encode -> decode: MISMATCH"
    exit 1
fi

if cmp -s test.cpio /tmp/verify_test.cpio; then
    echo "✓ encode -> verify: IDENTICAL"
else
    echo "✗ encode -> verify: MISMATCH"
    exit 1
fi

# Test with larger data (simulate TEE ramdisk)
echo ""
echo "--- Testing with larger data (32MB) ---"
dd if=/dev/urandom of=test_root/bigdata bs=1M count=32 2>/dev/null
cd test_root
find . | cpio -o -H newc --owner=0:0 > ../test_large.cpio
cd ..
python3 "$SCRIPT_DIR/.github/scripts/encode_lz4.py" test_large.cpio test_large.lz4
python3 "$SCRIPT_DIR/.github/scripts/decode_lz4.py" test_large.lz4 test_large_decoded.cpio
python3 "$SCRIPT_DIR/.github/scripts/verify_cpio.py" test_large.lz4 64 /tmp/verify_large.cpio

if cmp -s test_large.cpio test_large_decoded.cpio && cmp -s test_large.cpio /tmp/verify_large.cpio; then
    echo "✓ Large data round-trip: OK"
else
    echo "✗ Large data round-trip: FAILED"
    exit 1
fi

echo ""
echo "=== All tests passed! ==="