# Status

Live tracker — update this as work happens. `SPEC.md` is the frozen requirements
record; this file is the mutable "where are we right now."

**Last updated:** 2026-07-01

## Current phase

Pre-hardware-arrival. The Seeed Studio XIAO RP2040 has been ordered (see SPEC.md
§3, §4) but has not arrived. No firmware milestone can be gated/verified on
real hardware yet (flashing, enumeration checks, audio recording all require
the board in hand).

## Milestone progress (SPEC.md §12)

| Milestone | Gate | Status |
|---|---|---|
| M1 — Toolchain bring-up | Self-built UF2 flashes, LED blinks on custom timing | Not started — blocked on board arrival + OQ1 |
| M2 — HID keyboard standalone | Enumerates as keyboard, zero driver prompts, test keystroke lands | Not started |
| M3 — UAC2 mic standalone (synthetic tone) | Enumerates as audio input, tone recordable | Not started |
| M4 — Composite HID+UAC2 (highest risk) | Single device shows as both, zero drivers | Not started |
| M5 — Real mic integration | Recorded sample is intelligible speech | Not started — blocked on OQ2 (mic purchase) |
| M6 — Buttons/switch/gating/LED | End-to-end test inside real Claude Code session | Not started — blocked on OQ3/OQ4/OQ5 |
| M7 — Polish, freeze for PCB handoff | Pin map/parts/firmware frozen | Not started |

## What can happen before the board arrives

Firmware toolchain setup and skeleton project scaffolding don't require the
physical board — only flashing/testing does. See `firmware/README.md` for
current toolchain status.

## Open questions needing Geoff's input (SPEC.md §5)

- **OQ1** (blocks M1): toolchain — Pico SDK + TinyUSB vs. Arduino. Proceeding
  with Pico SDK + TinyUSB as the working default per the spec's own
  recommendation; flag for explicit confirmation.
- **OQ2** (blocks M5): mic part not yet purchased — SPH0645 (Adafruit #3421)
  recommended.
- **OQ3** (blocks M6): hardcode default Claude Code keys vs. target a custom
  `keybindings.json`.
- **OQ4** (blocks M6): push-to-talk + always-stream both active — proposed
  always-stream wins.
- **OQ5** (blocks M5/M6): silence vs. comfort noise when mic gated off.
- **OQ6** (blocks M4): which OSes need "no driver" validation beyond macOS.
- **OQ7** (non-blocking): no button for plan-mode's multi-option menu yet.

Each is tracked as its own GitHub issue — see repo issues list.

## Immediate next steps

1. Confirm OQ1 with Geoff (or proceed on the recommended default and flag it).
2. Set up Pico SDK + TinyUSB build environment (does not require the board).
3. When the board arrives: work through SPEC.md §4 action items (SKU/variant
   check) before anything else.
4. Purchase mic (OQ2) and buttons/switch (SPEC.md §7) — not urgent until M5/M6
   but lead time may be worth ordering now.
