# Claude Code Companion Peripheral

A single USB-C peripheral, built on a Seeed Studio XIAO RP2040, that
enumerates — with no driver install — as both a USB HID keyboard and a USB
Audio Class microphone at the same time. Physical controls handle push-to-talk
microphone activation, an always-on latch, and the keystrokes Claude Code uses
for its permission/approval prompts.

## Status

Pre-hardware-arrival, breadboard-planning phase. The RP2040 board has been
ordered but hasn't shipped yet. See [`docs/STATUS.md`](docs/STATUS.md) for the
live progress tracker.

## Start here

- [`docs/SPEC.md`](docs/SPEC.md) — the full project specification: verbatim
  requirements from the project owner, locked decisions, open questions, pin
  map, and the milestone-by-milestone work plan. This is the single source of
  truth; there is no other record of these requirements.
- [`docs/STATUS.md`](docs/STATUS.md) — current progress against the milestone
  plan and open questions.
- [`CLAUDE.md`](CLAUDE.md) — quick orientation for a coding agent picking this
  project up.

## Repo layout

```
docs/       spec + status
firmware/   RP2040 firmware (Pico SDK + TinyUSB)
hardware/   BOM, wiring notes, breadboard/PCB assets
```

## Hardware

- **MCU:** Seeed Studio XIAO RP2040 ([product page](https://www.seeedstudio.com/XIAO-RP2040-v1-0-p-5026.html), [wiki](https://wiki.seeedstudio.com/XIAO-RP2040/))
- **Mic:** I2S MEMS breakout (SPH0645 recommended, not yet purchased)
- **Controls:** 5 momentary buttons + 1 latching switch (see `docs/SPEC.md` §8 for the pin map)

## Work plan

See `docs/SPEC.md` §12 for the full milestone breakdown (M1–M7). In short:
toolchain bring-up → HID-only → UAC2-only (synthetic tone) → composite
HID+UAC2 device (highest-risk step) → real mic → buttons/gating/LED →
freeze for custom PCB handoff.
