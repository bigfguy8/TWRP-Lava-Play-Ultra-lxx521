# Changelog

## v3.0-lxx521 (2026-10-13)
**Status: TEE-ACTIVE, Community Test Pending**

- TEE-active: `teed`, `keymint`, `gatekeeper` HALs running
- SELinux permissive (`androidboot.selinux=permissive`)
- All TEE paths: `/mnt/twrp_t6/*` (rootfs-safe)
- `init.recovery`: 1736 bytes (TEE design)
- File count: 3464
- 4 TEE binaries, 13 libraries, 7 `.ta` files

### Bug #23 Fix
- Added `androidboot.selinux=permissive` to cmdline
- Reason: TWRP sepolicy lacks explicit `teed` rules
- Reference: `ref-vb.img` used same

### Safe Fallback Design
If `teed` fails → HALs don't start → TWRP boots without TEE → **NO BOOTLOOP**

---

## v1.6.1-safe-lxx521
**Status: Guaranteed Boot (no TEE)**

- TEE files present but all `.rc` / `.xml` renamed to `.disabled`
- Safe mode: standard `init.recovery` (no TEE services)

---

## v1.6.0-lxx521
**Status: FLASH-READY, ALL FIXED**

- CPIO padding bug fixed (`find . | cpio -o -H newc --owner=0:0`)
- Memory addresses corrected:
  - kernel: `0x40000000`
  - ramdisk: `0x66f00000`
  - tags: `0x47c80000`
- TEE files added (4 binaries, 13 libraries, 7 `.ta`)
- Size: 63,635,456 bytes, file count: 3472, `init.recovery`: 2001 bytes

---

## v1.5.1-lxx521
**Status: ❌ WRONG ADDRESSES**

- Used `--base 0x10000000` (default) instead of `--base 0x00000000`
- Kernel loaded at wrong address → bootloop

---

## v1.4-lxx521
**Status: ✅ + TEE files**

- TEE binaries + libraries + init scripts added
- File count increased

---

## v1.3-lxx521
**Status: ✅ CPIO FIXED**

- Fixed CPIO padding bug in Python repack
- `name_pad = (4 - ((110 + namesize) % 4)) % 4`
- Switched to Ubuntu `cpio` for repack

---

## v1.2-lxx521
**Status: ❌ TEE Bootloop**

- `mkdir /data/vendor/t6` failed on encrypted `/data`
- Fixed in v1.3: use `/tmp/vendor/t6` (tmpfs)

---

## v1.1-lxx521
**Status: ✅ Working Boot**

- First working TWRP for lxx521
- Fixed missing drivers from v1.0

---

## v1.0-lxx521
**Status: ❌ Missing Drivers**

- Initial build, many TWRP features broken
