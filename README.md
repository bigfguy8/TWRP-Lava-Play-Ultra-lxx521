# TWRP for Lava Play Ultra 5G (LXX521)

Unofficial TWRP build support for Lava Play Ultra 5G (LXX521, MediaTek MT6878, Android 15).

## Warning

Unofficial recovery. Bootloader unlock may erase data. Flashing a wrong image can bootloop or brick the device. Always keep your stock `vendor_boot.img` backup.

Do not flash `preloader`, `nvram`, `nvdata`, `modem`, or `persist`.

## Releases

| Version | Status | Download |
|---|---|---|
| v3.0.1-beta | Source audit; checksums verified | [Releases](https://github.com/bigfguy8/TWRP-Lava-Play-Ultra-lxx521/releases) |
| v3.0 | Experimental TEE build | [Download](https://github.com/bigfguy8/TWRP-Lava-Play-Ultra-lxx521/releases/tag/v3.0-lxx521) |
| v1.6.1-safe | No-TEE fallback build | [Download](https://github.com/bigfguy8/TWRP-Lava-Play-Ultra-lxx521/releases/tag/v1.6.1-safe-lxx521) |

## Verify release files

```bash
sha256sum -c SHA256SUMS.txt
```

Do not flash any file if checksum verification fails.
