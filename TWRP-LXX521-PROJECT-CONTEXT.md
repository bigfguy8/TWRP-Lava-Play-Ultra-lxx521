# TWRP Lava Play Ultra 5G (lxx521) — Project Context
Version: 1.6.0
Status: FLASH-READY
Last Updated: 2026-10-13

## Device
- Lava Play Ultra 5G (lxx521)
- MediaTek Dimensity 7300 (mt6878)
- Android 15, VNDK 14, Kernel 6.1.115
- vendor_boot partition: 64 MB
- TEE: TrustKernel (not Trustonic)

## Repositories
- Main: https://github.com/bigfguy8/TWRP-Lava-Play-Ultra-lxx521
- Device tree: https://github.com/fahimfrk/Dimensity7300-Device-Tree-Lava-Play-Ultra
- Kernel: https://github.com/SiliconxLab/android_device_lava_lxx521-kernel (lineage-23.2)

## Version History
| Ver | Status | Feature | SHA256 |
|-----|--------|---------|--------|
| v1.0 | ❌ | Missing drivers | d5ddac07... |
| v1.1 | ✅ | Working boot | d5ddac07... |
| v1.2 | ❌ | CPIO bug | bbf5fe02... |
| v1.3 | ✅ | CPIO fixed | fe0b740b... |
| v1.4 | ✅ | + TEE files | — |
| v1.5.1 | ⚠️ | Wrong addresses | f91496da... |
| v1.6.0 | ✅ | ALL FIXED | 30aff209... |

## Critical Fixes Applied

### Fix 1: Python CPIO Padding
WRONG: name_pad = (4 - (namesize % 4)) % 4
RIGHT: name_pad = (4 - ((110 + namesize) % 4)) % 4
Solution: Use Ubuntu cpio:
  find . | cpio -o -H newc --owner=0:0 > ramdisk01.cpio

### Fix 2: Memory Addresses
AOSP mkbootimg.py defaults to --base 0x10000000
Must add: --base 0x00000000
Correct addresses:
- kernel: 0x40000000
- ramdisk: 0x66f00000
- tags: 0x47c80000

### Fix 3: TEE Bootloop (v1.2)
Was: mkdir /data/vendor/t6 (fails on encrypted /data)
Now: mkdir /tmp/vendor/t6 (tmpfs, always writable)

## Verified Parameters (v1.6.0)
- kernel load: 0x40000000
- ramdisk load: 0x66f00000
- tags: 0x47c80000
- dtb: 0x47c80000
- header_version: 4
- pagesize: 4096
- cmdline: bootopt=64S3,32N2,64N2
- Size: 63,635,456 bytes
- init.recovery: 2001 bytes
- File count: 3472

## Build Workflow (GitHub Actions)
File: .github/workflows/main.yml
Trigger:
  gh workflow run main.yml \
    --repo bigfguy8/TWRP-Lava-Play-Ultra-lxx521 \
    --ref main \
    -f version="v1.6.1-test" \
    -f enable_tee=true \
    -f create_release=false

Flow:
1. Checkout repo
2. Pre-flight file check
3. Install cpio, libarchive-tools, lz4, python3
4. repo init -b twrp-12.1
5. Sync + clone device tree
6. mka recoveryimage vendorbootimage -j2
7. Extract ramdisk01 from build
8. Decode LZ4 legacy
9. Inject TEE (if enabled)
10. Swap init.recovery to TEE version
11. Repack with cpio
12. LZ4 HC compress
13. mkbootimg with --base 0x00000000
14. Verify (file count >= 3400, init.recovery >= 200, header=VNDRBOOT)
15. Independent verify
16. Release (if create_release=true)

## TEE Stack Components
Binaries:
- /vendor/bin/teed (55 KB)
- /vendor/bin/tee_check_keybox
- /vendor/bin/hw/android.hardware.security.keymint@3.0-service.trustkernel (104 KB)
- /vendor/bin/hw/android.hardware.gatekeeper-service.trustkernel (25 KB)

Libraries (13):
- libteec.so, libTEECommon.so, libkeymint.so
- lib_android_keymaster_keymint_utils.so
- android.hardware.security.keymint-V3-ndk.so
- android.hardware.gatekeeper-V1-ndk.so
- (etc)

Trusted Applications (7 .ta files):
- 02662e8e-e126-11e5-b86d9a79f06e9478.ta
- 4545534d-*.ta (3 files)
- 9ef77781-*.ta
- b46325e6-*.ta
- e97c270e-*.ta

Init Scripts:
- /vendor/etc/init/trustkernel.rc
- /vendor/etc/init/android.hardware.security.keymint@3.0-service.trustkernel.rc
- /vendor/etc/init/android.hardware.gatekeeper-service.trustkernel.rc

## Flash Instructions

### Pre-Flash
- Battery >= 70%
- Backup stock vendor_boot.img (SHA256: 4242b560...)
- Backup stock vbmeta*.img

### Method A: mtkclient (root)
mtk r vendor_boot_a vendor_boot_stock.img  # Backup first!
mtk w vendor_boot_a twrp_lxx521_v1.6.0.img
mtk reset

### Method B: SP Flash Tool (PC)
1. Open SPFlashToolV6.exe as admin
2. Choose → MT6878_Android_scatter.xml
3. Set vendor_boot_a → twrp_lxx521_v1.6.0.img
4. Tick ONLY vendor_boot_a
5. Download
6. Phone OFF → Vol+ + Vol- → USB

### Method C: Fastboot
fastboot flash vendor_boot twrp_lxx521_v1.6.0.img
fastboot reboot recovery

## Recovery if Fail
mtk w vendor_boot_a vendor_boot_stock.img
mtk reset

## Key Stock SHAs
vendor_boot.img: 4242b5600d5d39e12fb1f04c6fa422f33f8bdfa27ce189b3b61426907b3c31eb
ramdisk00: 25b7004d1dc841c3328fefea6e327a2f1e18068ade02352a0a0e3cf78f127215
dtb: c502c7bc555e2440ecdca8053c6abea37f48855fdee4453e966a466238ec8bb2

## Key Scripts
~/analyze/decode_legacy_lz4.py — LZ4 legacy decoder
~/analyze/encode_legacy_lz4.py — LZ4 HC legacy encoder
~/analyze/extract_cpio.py — Python CPIO extractor

## New Device Setup (Termux)
pkg update -y && \
pkg install -y git gh python python-pip curl && \
pip install lz4 pyyaml && \
gh auth login && \
git clone https://github.com/bigfguy8/TWRP-Lava-Play-Ultra-lxx521.git

## Community
- Telegram: t.me/playultra5g
- GitHub Issues: https://github.com/bigfguy8/TWRP-Lava-Play-Ultra-lxx521/issues
