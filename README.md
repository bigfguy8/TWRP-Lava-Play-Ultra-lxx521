# TWRP for Lava Play Ultra 5G (LXX521)

**Unofficial TWRP recovery for the Lava Play Ultra 5G (LXX521), powered by MediaTek MT6878 (Dimensity 7300) and Android 15.**

<a href="https://github.com/bigfguy8/TWRP-Lava-Play-Ultra-lxx521/actions/workflows/main.yml">
  <img src="https://github.com/bigfguy8/TWRP-Lava-Play-Ultra-lxx521/actions/workflows/main.yml/badge.svg" alt="Build Status">
</a>

---

## ⚠️ Critical Warning

**This is an unofficial recovery. Proceed at your own risk.**

- **Unlocking the bootloader will erase all user data** on the device.
- **Flashing an incorrect image can bootloop or hard-brick your device.**
- **Always keep a backup of your stock `vendor_boot.img`** before flashing any custom recovery.
- **NEVER flash** the following partitions under any circumstances: `preloader`, `nvram`, `nvdata`, `modem`, `persist`. Flashing these can permanently damage the device.
- TEE mode selection is critical: flashing the wrong TEE configuration can result in data loss or bootloops.

---

## 📦 TEE Modes

The build supports three TEE configuration modes. Choose the one that matches your use case:

| Mode | Description | Use Case |
|------|-------------|----------|
| **Safe** | TEE services injected without `.disabled` init rc files. Decryption works via stock init.recovery. | Default for most users who want decryption + basic TEE services. |
| **TEE Active** | Custom `init.recovery.mt6878.rc.tee` replaces the standard init. TEE services are activated. | Advanced users requiring TEE-specific features; **can bootloop if incompatible**. |
| **No TEE** | No TEE files or binaries injected. Stock recovery behavior without TrustKernel TEE. | Users who do not need TEE and want the simplest, most stable build. |

---

## 🏷️ Releases & Build Options

| Version | Base | TEE Mode | Status | Download |
|---------|------|----------|--------|----------|
| **v3.2.0+** | `twrp-14.1` | Inject TEE, modernized build | Stable | [Releases](https://github.com/bigfguy8/TWRP-Lava-Play-Ultra-lxx521/releases) |
| **v3.0.1-beta** | `twrp-12.1` | Source audit; checksums verified | Beta | [Releases](https://github.com/bigfguy8/TWRP-Lava-Play-Ultra-lxx521/releases) |
| **v3.0** | `twrp-12.1` | TEE Active (custom init.recovery) | Experimental | [v3.0-lxx521](https://github.com/bigfguy8/TWRP-Lava-Play-Ultra-lxx521/releases/tag/v3.0-lxx521) |
| **v1.6.1-safe** | `twrp-12.1` | No-TEE fallback build | Guaranteed boot | [v1.6.1-safe-lxx521](https://github.com/bigfguy8/TWRP-Lava-Play-Ultra-lxx521/releases/tag/v1.6.1-safe-lxx521) |

### Build Configuration (GitHub Actions)

The build is driven by `.github/workflows/main.yml` with the following options:

- **`enable_tee`** — Inject TEE files (TrustKernel TEE binaries/libraries). Default: `true`.
- **`tee_activation`** — Replace `init.recovery` with TEE-active version. Requires `enable_tee=true`. Default: `false` (Safer).
- **`twrp_branch`** — TWRP manifest branch. Options: `twrp-12.1`, `twrp-14`, `twrp-14.1`. Default: `twrp-14.1`.
- **`create_release`** — Automatically create a GitHub release after a successful build.

---

## 🚀 Installation & Flashing

1. **Backup your stock `vendor_boot.img`** and verify its SHA256 checksum.
2. Ensure battery is at least **70% charged**.
3. Boot into fastboot mode: `adb reboot fastboot`.
4. Flash the recovery using **mtkclient**:

```bash
# Flash vendor_boot partition (TWRP is flashed to vendor_boot)
python mtk.py w vendor_boot_a twrp_lxx521_<VERSION>.img
python mtk.py reset
