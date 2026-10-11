# TWRP for Lava Play Ultra 5G (lxx521)

Custom TWRP recovery for **Lava Play Ultra 5G** (lxx521 / MediaTek Dimensity 7300).

## Downloads

| Version | Status | Link |
|---|---|---|
| v1.1 | ✅ Recommended | [Release](https://github.com/bigfguy8/TWRP-Lava-Play-Ultra-lxx521/releases/tag/v1.1-lxx521) |
| v1.0 | ⚠️ Broken (bootloop) | [Release](https://github.com/bigfguy8/TWRP-Lava-Play-Ultra-lxx521/releases/tag/v1.0-lxx521) |

## Device Specs

- Device: Lava Play Ultra 5G
- Codename: lxx521
- SoC: MediaTek Dimensity 7300 (mt6878)
- Android: 15 / VNDK 14
- Kernel: 6.1.115
- Storage: UFS 3.1, Virtual A/B

## Build

Uses GitHub Actions workflow (`.github/workflows/main.yml`).

- Manifest: `twrp-12.1`
- Build time: ~59 minutes
- Lunch: `twrp_lxx521-eng`

## Testing

See [TESTING.md](TESTING.md) for testing instructions.

## Credits

- Device tree: fahimfrk
- Kernel: SiliconxLab
- Built with: AOSP mkbootimg, TWRP minimal manifest

## Warning

**For advanced users only.** Always back up stock vendor_boot.img before flashing.
