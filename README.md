# TWRP for Lava Play Ultra 5G (LXX521)

**Unofficial TWRP recovery for the Lava Play Ultra 5G (LXX521), powered by MediaTek MT6878 (Dimensity 7300) and Android 15.**

[![Build TWRP](https://github.com/bigfguy8/TWRP-Lava-Play-Ultra-lxx521/actions/workflows/main.yml/badge.svg)](https://github.com/bigfguy8/TWRP-Lava-Play-Ultra-lxx521/actions/workflows/main.yml)

---

## ⚠️ Critical Warning

> **This is an unofficial recovery.**
> - Unlocking the bootloader **will erase all user data**.
> - Flashing an incorrect image can **bootloop or hard-brick** your device.
> - **ALWAYS keep a backup of your stock `vendor_boot.img`** before proceeding.
> - **NEVER flash** `preloader`, `nvram`, `nvdata`, `modem`, or `persist` partitions.

---

## 📦 Releases & Versions

| Version | Base | Status | Download |
| :--- | :--- | :--- | :--- |
| **v3.2.0+** | `twrp-14.1` | TEE injection, modernized build | [Releases](https://github.com/bigfguy8/TWRP-Lava-Play-Ultra-lxx521/releases) |
| **v3.0.1-beta** | `twrp-12.1` | Source audit; checksums verified | [Releases](https://github.com/bigfguy8/TWRP-Lava-Play-Ultra-lxx521/releases) |
| **v3.0** | `twrp-12.1` | Experimental TEE build | [Download](https://github.com/bigfguy8/TWRP-Lava-Play-Ultra-lxx521/releases/tag/v3.0-lxx521) |
| **v1.6.1-safe** | `twrp-12.1` | No-TEE fallback build | [Download](https://github.com/bigfguy8/TWRP-Lava-Play-Ultra-lxx521/releases/tag/v1.6.1-safe-lxx521) |

### ✅ Verify Release Files

Always verify the integrity of your download before flashing:

```bash
sha256sum -c SHA256SUMS