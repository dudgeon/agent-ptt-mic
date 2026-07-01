# Hardware

Breadboard phase — see `docs/SPEC.md` §7 (BOM) and §8 (pin map).

## Bill of materials

| Part | Status |
|---|---|
| Seeed Studio XIAO RP2040 | Ordered, not arrived |
| I2S MEMS mic (SPH0645 recommended) | Not yet purchased (OQ2) |
| 5× tactile momentary switches | Not yet purchased |
| 1× slide/toggle switch (always-stream latch) | Not yet purchased |
| Breadboard + jumper wires | Not yet purchased |
| Data-capable USB-C cable | Not yet purchased |

## Pin map

See `docs/SPEC.md` §8 for the full XIAO-pad-to-GPIO table and the
constraints driving it (consecutive-GPIO requirement for I2S BCLK/LRCLK,
active-low buttons via internal pull-ups, active-low onboard LEDs).

This directory will hold breadboard photos, wiring notes, and eventually
custom PCB design files once the Milestone 7 gate (`docs/SPEC.md` §12) is
reached — no PCB work before then.
