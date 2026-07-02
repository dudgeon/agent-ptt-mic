# Status

Live tracker — update this as work happens. `SPEC.md` is the frozen requirements
record; this file is the mutable "where are we right now."

**Last updated:** 2026-07-02

## Current phase

Two concurrent tracks:

1. **Breadboard firmware track (M1–M7, SPEC.md §12).** Pre-hardware-arrival —
   the Seeed Studio XIAO RP2040 has been ordered (see SPEC.md §3, §4) but has
   not arrived. No firmware milestone can be gated/verified on real hardware
   yet (flashing, enumeration checks, audio recording all require the board
   in hand).
2. **PCB / industrial-design track (SPEC.md §16).** Design spike Geoff
   requested while awaiting delivery; runs in parallel with (not instead of)
   the breadboard plan. **First full design pass complete (2026-07-02),
   then revised same day (v2):** Geoff confirmed the XIAO he ordered is the
   **pre-soldered/header SKU** (answers issue #9 ahead of physical arrival —
   still worth a visual check on arrival that it's the RP2040 family member)
   and asked to cut unnecessary SMD scope. Every active part is now
   through-hole/header-mount — hand-solderable, no reflow/hot-air anywhere —
   at the cost of a thicker enclosure (~22.6mm vs. ~14.3mm). See
   `docs/PHYSICAL_DESIGN_SPEC.md` §7 for the full rationale and the
   deviations awaiting Geoff's confirmation. The vendor-sourcing research
   (`hardware/ASSEMBLY_SOURCING.md`) and cost artifact
   (`hardware/assembly_options.html`) predate this revision and need
   re-checking — tracked as [#15](https://github.com/dudgeon/agent-ptt-mic/issues/15).
   Remaining: layout sign-off, PCB routing + pre-fab footprint
   verification, first fit-check print.

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

- **OQ1** (blocks M1, [#2](https://github.com/dudgeon/agent-ptt-mic/issues/2)):
  toolchain — Pico SDK + TinyUSB vs. Arduino. Proceeding with Pico SDK +
  TinyUSB as the working default per the spec's own recommendation; flag for
  explicit confirmation.
- **OQ2** (blocks M5, [#3](https://github.com/dudgeon/agent-ptt-mic/issues/3)):
  mic part not yet purchased — SPH0645 (Adafruit #3421) recommended.
- **OQ3** (blocks M6, [#4](https://github.com/dudgeon/agent-ptt-mic/issues/4)):
  hardcode default Claude Code keys vs. target a custom `keybindings.json`.
- **OQ4** (blocks M6, [#5](https://github.com/dudgeon/agent-ptt-mic/issues/5)):
  push-to-talk + always-stream both active — proposed always-stream wins.
- **OQ5** (blocks M5/M6, [#6](https://github.com/dudgeon/agent-ptt-mic/issues/6)):
  silence vs. comfort noise when mic gated off.
- **OQ6** (blocks M4, [#7](https://github.com/dudgeon/agent-ptt-mic/issues/7)):
  which OSes need "no driver" validation beyond macOS.
- **OQ7** (non-blocking, [#8](https://github.com/dudgeon/agent-ptt-mic/issues/8)):
  no button for plan-mode's multi-option menu yet.
- **Board arrival checklist** (blocks M1, [#9](https://github.com/dudgeon/agent-ptt-mic/issues/9)):
  confirm SKU/variant the moment the XIAO RP2040 lands.
- **Button-count reconciliation** (blocks M6, [#10](https://github.com/dudgeon/agent-ptt-mic/issues/10)):
  "three buttons" verbatim vs. the 6-control pin map — not yet re-confirmed.

Milestone progress is also tracked as a checklist in
[#1](https://github.com/dudgeon/agent-ptt-mic/issues/1).

## Immediate next steps

### Breadboard track
1. Confirm OQ1 with Geoff (or proceed on the recommended default and flag it).
2. Set up Pico SDK + TinyUSB build environment (does not require the board).
3. When the board arrives: work through SPEC.md §4 / issue #9 (SKU/variant
   check) before anything else.
4. Purchase mic (OQ2) and buttons/switch (SPEC.md §7) — not urgent until M5/M6
   but lead time may be worth ordering now.

### PCB / industrial-design track
1. Geoff reviews the mockup renders (`hardware/mockup/output/renders/`) and
   confirms/adjusts the layout deviations in `docs/PHYSICAL_DESIGN_SPEC.md`
   §7 (thumb PTT, 2×2 grid, right-side latch).
2. Route the carrier board in an interactive KiCad session and work the
   pre-fab VERIFY list in `hardware/pcb/README.md`.
3. FDM fit-check print of the two shell parts (checklist at the end of
   `hardware/enclosure/README.md`). Ordering parts/fab needs Geoff's
   go-ahead first.
