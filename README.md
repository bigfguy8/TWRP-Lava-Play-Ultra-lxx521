# TWRP for Lava Play Ultra 5G (lxx521)

Unofficial community recovery project for the Lava Play Ultra 5G. This is an advanced, device-specific project—not an official Lava or TWRP release.

> **Warning:** Recovery images can cause data loss, boot loops, or an unusable device if they are incompatible. Use only after confirming the exact device and having a tested way to restore stock firmware.

## Device target

- **Model:** Lava Play Ultra 5G
- **Codename:** `lxx521`
- **SoC:** MediaTek Dimensity 7300 (`mt6878`)
- **Platform details in this project:** Android 15 / VNDK 14, kernel 6.1.115, UFS 3.1, Virtual A/B

Do not use these images on another model or variant.

## Releases

| Version | Project notes | Download |
|---|---|---|
| **v3.0** | TEE-active; marked as a community test and experimental | [Release](https://github.com/bigfguy8/TWRP-Lava-Play-Ultra-lxx521/releases/tag/v3.0-lxx521) |
| **v1.6.1-safe** | Non-TEE variant; “safe” is a project label, not a guarantee that it will boot | [Release](https://github.com/bigfguy8/TWRP-Lava-Play-Ultra-lxx521/releases/tag/v1.6.1-safe-lxx521) |

The project marks v1.5.1 as having wrong addresses, v1.2 as bootlooping, and v1.0 as missing drivers. Avoid those builds. Check the release notes before downloading any image.

## Build

The documented build uses GitHub Actions and the TWRP 12.1 manifest. The target is `twrp_lxx521-eng`. There is no supported on-device Termux build procedure documented here.

The workflow has TEE options. Keep `enable_tee` and `tee_activation` disabled unless you understand the risks and have verified the required files for this exact device. TEE activation is specifically marked risky in the workflow.

Do not treat a successful CI build as proof that an image will boot, decrypt data, or be safe to flash. The workflow should pass its checks, and the image should be independently verified and tested before use.

## Before testing or flashing

1. Confirm the phone is exactly the Lava Play Ultra 5G (`lxx521`).
2. Back up personal data.
3. Back up the original `vendor_boot.img` and relevant `vbmeta` images. Keep copies off the phone and verify that they are readable.
4. Have a tested stock-restoration method and the required tools ready before making changes.
5. Charge the phone to at least 70%.
6. Read [TESTING.md](TESTING.md) and the release notes. Verify the complete image checksum if one is provided; do not rely on a truncated checksum.
7. Confirm the exact partition and slot for your firmware before writing anything. Never guess a partition or flash to `recovery` based on instructions for another device.

## Testing and recovery

Use [TESTING.md](TESTING.md) as a checklist, not as a guarantee of safety. Check that TWRP boots, touch works, internal storage shows its real size, and Android can be reached again. If the device bootloops or storage is unavailable, stop testing and use your verified stock-restoration procedure.

## Reporting an issue

When opening an issue, include:

- Exact device model and codename
- Recovery version and full SHA-256, if available
- Whether the device booted and whether touch worked
- Internal storage result
- Relevant recovery logs and screenshots
