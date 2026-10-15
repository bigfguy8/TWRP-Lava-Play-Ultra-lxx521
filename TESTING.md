# TWRP Testing Guide — Lava Play Ultra 5G (lxx521)

## Latest Release
- **v3.0** (TEE-active, community test): https://github.com/bigfguy8/TWRP-Lava-Play-Ultra-lxx521/releases/tag/v3.0-lxx521
- v1.6.1-safe (guaranteed boot, no TEE): https://github.com/bigfguy8/TWRP-Lava-Play-Ultra-lxx521/releases/tag/v1.6.1-safe-lxx521

## Before Flashing
1. Battery >= 70%
2. Backup stock `vendor_boot.img` — **SHA256: `4242b5600d5d...`**
3. Backup stock `vbmeta*.img`
4. Have mtkclient or SP Flash Tool ready for recovery

## Flash
- `mtk w vendor_boot_a twrp_lxx521_v3.0.img` → `mtk reset`
- Do **NOT** flash to recovery partition.

## Post-Flash Test Matrix

| # | Test | Expected (PASS) | Fail Meaning |
|---|------|------|---|
| 1 | Phone boots into TWRP | TWRP UI, no bootloop | Bootloop → flash stock |
| 2 | Touch works | Responsive | TWRP touch missing |
| 3 | **Internal Storage** | Shows real GB, **NOT 0MB** | 0MB = TEE fail |
| 4 | FBE decrypt | Files visible in Internal Storage | Data not decrypted |
| 5 | Backup / Restore | Works to SD / OTG | Feature broken |
| 6 | ADB sideload | `adb sideload` works | Not supported |
| 7 | OTG mount | USB stick accessible | Storage init missing |
| 8 | Reboot to system | Boots back to Android | Bootchain broken |

## THE KEY TEE TEST (v3.0)

After flashing, open TWRP → **Install → Select Storage → Internal Storage**:
- **0MB** → TEE fail → collect log (below)
- **Real size** → TEE working → success

## Log Collection

```bash
# Pull recovery log
adb pull /tmp/recovery.log

# TEE-specific log
adb pull /tmp/recovery_tee.log
```

## TEE Status Check (from shell / TWRP terminal)

```bash
# Verify teed running
getprop | grep -i trustkernel
getprop | grep -i teed

# Verify keymint + gatekeeper
getprop | grep keymint
getprop | grep gatekeeper
```

## Recovery if Fail

```bash
mtk w vendor_boot_a vendor_boot_stock.img
mtk reset
```

## Report Issues

Create an issue: https://github.com/bigfguy8/TWRP-Lava-Play-Ultra-lxx521/issues

Include:
- Build version + SHA256
- Boot status (PASS/FAIL)
- Internal storage size (0MB or real MB)
- `recovery.log` + `recovery_tee.log`
- Screenshots
