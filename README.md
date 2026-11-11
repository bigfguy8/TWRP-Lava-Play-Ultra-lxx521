# TWRP for Lava Play Ultra 5G (LXX521)

Unofficial TWRP build support for Lava Play Ultra 5G (LXX521, MediaTek MT6878/Dimensity 7300, Android 15).

## ⚠️ Warning

**Unofficial recovery.** Bootloader unlock may erase data. Flashing a wrong image can bootloop or brick the device. **Always keep your stock `vendor_boot.img` backup.**

Do not flash `preloader`, `nvram`, `nvdata`, `modem`, or `persist`.

## Releases

| Version | Base | Status | Download |
|---|---|---|---|
| v3.2.0+ | twrp-14.1 | TEE injection, modernized build | [Releases](https://github.com/bigfguy8/TWRP-Lava-Play-Ultra-lxx521/releases) |
| v3.0.1-beta | twrp-12.1 | Source audit; checksums verified | [Releases](https://github.com/bigfguy8/TWRP-Lava-Play-Ultra-lxx521/releases) |
| v3.0 | twrp-12.1 | Experimental TEE build | [Download](https://github.com/bigfguy8/TWRP-Lava-Play-Ultra-lxx521/releases/tag/v3.0-lxx521) |
| v1.6.1-safe | twrp-12.1 | No-TEE fallback build | [Download](https://github.com/bigfguy8/TWRP-Lava-Play-Ultra-lxx521/releases/tag/v1.6.1-safe-lxx521) |

## Verify Release Files

```bash
sha256sum -c SHA256SUMS
```

Do not flash any file if checksum verification fails.

## Building from Source

### Quick Start (GitHub Actions)

1. Go to **Actions** → **Build TWRP (Verify-First)** → **Run workflow**
2. Configure options:
   - **Version**: e.g., `v3.2.0`
   - **TWRP Branch**: `twrp-14.1` (recommended, Android 14 base), `twrp-14`, or `twrp-12.1`
   - **Enable TEE**: `true` (injects TrustKernel TEE binaries)
   - **TEE Activation**: `false` (safe mode, TEE files present but inactive) or `true` (⚠️ replaces init.recovery, risky)
   - **Create Release**: `true` to auto-create GitHub release
   - **Skip Verify**: `false` (independent verification recommended)

### Build Options Explained

| Option | Description | Risk |
|---|---|---|
| `twrp_branch` | TWRP manifest branch. `twrp-14.1` = Android 14 base (recommended for Android 15 device) | Low |
| `enable_tee` | Inject TrustKernel TEE binaries (teed, keymint, gatekeeper, trusted apps) | Low |
| `tee_activation` | **Dangerous**: Replaces init.recovery with TEE-enabled version. May bootloop if incompatible. | **High** |
| `create_release` | Auto-create GitHub release after successful build + verify | None |
| `skip_verify` | Skip independent verify job (faster, less safe) | Medium |

### TEE Modes

| Mode | `enable_tee` | `tee_activation` | Behavior |
|---|---|---|---|
| **Safe (Default)** | `true` | `false` | TEE files injected but `.disabled`; standard init.recovery used |
| **TEE Active** | `true` | `true` | Custom init.recovery starts `teed`, keymint, gatekeeper services |
| **No TEE** | `false` | `false` | Standard TWRP, no TEE files |

### Flashing

```bash
# Flash to vendor_boot partition (slot A)
mtk w vendor_boot_a twrp_lxx521_v3.2.0.img
mtk reset
```

Or use `fastboot flash vendor_boot_a twrp_lxx521_v3.2.0.img` if fastbootd works.

## Project Structure

```
.
├── .github/
│   ├── workflows/main.yml      # Build workflow (configurable via inputs)
│   └── scripts/                # LZ4 encode/decode/verify utilities
├── tee-files/                  # TrustKernel TEE binaries (injected at build)
│   ├── bin/                    # teed, tee_check_keybox
│   ├── bin-hw/                 # keymint, gatekeeper HAL services
│   ├── lib64/                  # TEE shared libraries
│   ├── etc-init/               # init.rc files (copied as .disabled unless tee_activation)
│   ├── etc-vintf/              # VINTF manifests
│   └── app-t6/                 # Trusted applications (.ta files)
├── stock-files/                # Stock vendor_ramdisk00.lz4 + dtb.img (required)
└── CHANGELOG.md
```

## Stock Files Required

Place in `stock-files/`:
- `vendor_ramdisk00.lz4` — Stock vendor ramdisk (fragment 0)
- `dtb.img` — Device tree blob
- `SHA256SUMS` — Optional checksums for verification

Extract from stock firmware using:
```bash
# Example: extract from payload.bin
python3 extract_android_ota_payload.py payload.bin --partition vendor_boot --output vendor_boot.img
python3 unpack_bootimg.py --boot_img vendor_boot.img --out .
# vendor_ramdisk00.lz4 is fragment 0, dtb.img from --dtb
```

## Upgrading TWRP Base

The workflow supports multiple TWRP manifest branches:
- **twrp-14.1** (recommended) — Android 14 QPR base, best for Android 15 devices
- **twrp-14** — Android 14 base
- **twrp-12.1** — Android 12.1 base (legacy)

To upgrade:
1. Run workflow with desired `twrp_branch`
2. Test thoroughly (TEE, decryption, backup/restore, ADB, MTP)
3. Report issues with logs

## TEE Trusted Applications

The `tee-files/app-t6/` directory contains TrustKernel trusted applications:
- `cfg.ini` — TEE configuration
- `*.ta` — Trusted applications (keymaster, gatekeeper, etc.)
- `data/` — Prebuilt TEE filesystem data

These are injected into `/vendor/app/t6/` in the recovery ramdisk.

## Verification

The build pipeline includes:
1. **Internal Verify** — Runs in build job: header check, size limit, CPIO integrity, file count, TEE presence
2. **Independent Verify** — Separate job: re-downloads artifact, re-verifies everything
3. **Release** — Only creates release if both verifications pass

## Troubleshooting

| Issue | Solution |
|---|---|
| Build fails at `repo sync` | Check network, try `twrp-12.1` branch first |
| `vendor_boot.img` too large | Reduce TEE files or check ramdisk size |
| Bootloop after flash | Flash stock `vendor_boot.img`, try `tee_activation=false` |
| TEE services not starting | Check `init.recovery.mt6878.rc.tee` compatibility |
| Verification fails | Ensure stock files match device exactly |

## Changelog

See [CHANGELOG.md](CHANGELOG.md) for detailed version history.

## Credits

- TWRP Team
- [minimal-manifest-twrp](https://github.com/minimal-manifest-twrp)
- [fahimfrk](https://github.com/fahimfrk) — Device tree
- [SiliconxLab](https://github.com/SiliconxLab) — Kernel prebuilts
- TrustKernel — TEE implementation

## License

Apache-2.0 / GPL-2.0 (kernel). See individual files for licenses.