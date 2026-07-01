# Firmware

Empty for now — no toolchain has been installed or firmware written yet.
This directory is scaffolding for Milestone 1 onward (see `docs/SPEC.md` §12).

## Planned toolchain (OQ1, proposed default)

**Pico SDK (C) + TinyUSB**, per `docs/SPEC.md` §5 OQ1. This is where the
reference USB Audio Class examples live (`uac2_headset`, `audio_4_channel_mic`)
and gives direct control over the composite USB descriptor needed for M4.
Not yet explicitly re-confirmed by the project owner — flagged in
`docs/STATUS.md`.

## Setup (once OQ1 is confirmed)

1. Install the [Pico SDK](https://github.com/raspberrypi/pico-sdk) and the
   `arm-none-eabi` toolchain.
2. TinyUSB is vendored as a submodule of the Pico SDK — no separate install.
3. Project layout will follow the standard Pico SDK CMake structure
   (`CMakeLists.txt` + `pico_sdk_import.cmake` at this directory's root).

None of this requires the physical board to be in hand — only flashing and
enumeration testing (M1's gate onward) do.

## Milestone-to-code mapping (planned)

- `m1_blink/` — minimal blink to prove the toolchain and flashing process
- `m2_hid/` — HID keyboard only
- `m3_uac2/` — UAC2 mic only, synthetic sine tone
- `m4_composite/` — merged HID + UAC2 composite descriptor
- `m5_mic/` — real I2S mic via PIO
- `m6_controls/` — buttons, switch, gating logic, status LED

These don't exist yet; created as each milestone starts.
