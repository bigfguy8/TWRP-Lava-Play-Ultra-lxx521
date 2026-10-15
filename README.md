# TWRP for Lava Play Ultra 5G (lxx521)

Custom TWRP recovery for **Lava Play Ultra 5G** (lxx521 / MediaTek Dimensity 7300).

## Downloads

| Version | Status | Link |
|---|---|---|
| **v3.0** | ✅ TEE-Active, Community Test | [Release](https://github.com/bigfguy8/TWRP-Lava-Play-Ultra-lxx521/releases/tag/v3.0-lxx521) |
| v1.6.1-safe | ✅ Guaranteed Boot (no TEE) | [Release](https://github.com/bigfguy8/TWRP-Lava-Play-Ultra-lxx521/releases/tag/v1.6.1-safe-lxx521) |
| v1.6.0 | ✅ Flash-Ready | [Release](https://github.com/bigfguy8/TWRP-Lava-Play-Ultra-lxx521/releases/tag/v1.6.0-lxx521) |
| v1.5.1 | ⚠️ Wrong addresses | [Release](https://github.com/bigfguy8/TWRP-Lava-Play-Ultra-lxx521/releases/tag/v1.5.1-lxx521) |
| v1.2 | ❌ Bootloop | [Release](https://github.com/bigfguy8/TWRP-Lava-Play-Ultra-lxx521/releases/tag/v1.2-lxx521) |
| v1.1 | ✅ Working boot | [Release](https://github.com/bigfguy8/TWRP-Lava-Play-Ultra-lxx521/releases/tag/v1.1-lxx521) |
| v1.0 | ❌ Missing drivers | [Release](https://github.com/bigfguy8/TWRP-Lava-Play-Ultra-lxx521/releases/tag/v1.0-lxx521) |

## Device Specs

- Device: Lava Play Ultra 5G
- Codename: lxx521
- SoC: MediaTek Dimensity 7300 (mt6878)
- Android: 15 / VNDK 14
- Kernel: 6.1.115
- Storage: UFS 3.1, Virtual A/B
- TEE: TrustKernel (not Trustonic)

## v3.0 Features

- TEE-active: teed + keymint + gatekeeper HALs
- SELinux permissive
- File count: 3464, init.recovery: 1736 bytes
- 4 TEE binaries, 13 libraries, 7 .ta files

## Build

Uses GitHub Actions workflow (`.github/workflows/main.yml`).

- Manifest: `twrp-12.1`
- Build time: ~59 minutes
- Lunch: `twrp_lxx521-eng`

### Build Triggers

- **Safe (no TEE):** `enable_tee=false` → guaranteed boot
- **TEE files present, inactive:** `enable_tee=true, tee_activation=false`
- **TEE active:** `enable_tee=true, tee_activation=true` → TEE services running

## Testing

See [TESTING.md](TESTING.md) for testing instructions.

## Changelog

See [CHANGELOG.md](CHANGELOG.md) for full version history.

## Credits

- Device tree: fahimfrk
- Kernel: SiliconxLab
- Built with: AOSP mkbootimg, TWRP minimal manifest

## Warning

**For advanced users only.** Always back up stock `vendor_boot.img` before flashing.
If TWRP fails to boot, flash the stock backup immediately:

```
mtk w vendor_boot_a vendor_boot_stock.img
mtk reset
```
