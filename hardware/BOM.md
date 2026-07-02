# Bill of Materials — Carrier PCB Track (v2)

Final part selections for the custom carrier PCB + handheld enclosure track
(`docs/PHYSICAL_DESIGN_SPEC.md`). The breadboard track's BOM in
`docs/SPEC.md` §7 is separate and unchanged.

**v2 revision (2026-07-02):** the XIAO Geoff actually ordered is the
**pre-soldered/header** SKU (`docs/SPEC.md` §4), not the bare-castellated
one v1 assumed — it mounts via its own presoldered pin headers, not a
flush reflow joint. At the same time, the mic switched from a bare SMD
chip to a breakout module (matching the original breadboard-track part),
and the status LED switched from an addressable SMD WS2812B to a plain
THT LED. Net effect: **every active part on this board is now
through-hole/header-mount — hand-solderable with a plain iron, no reflow
or hot-air anywhere** — at the cost of a thicker enclosure (~22.6mm vs.
~14.3mm in v1), since the header-mounted module needs real standoff
clearance instead of sitting flush. See
`hardware/assembly_options.html` for the cost/effort comparison this
enables, and `docs/PHYSICAL_DESIGN_SPEC.md` §7 for the full rationale.

Per project convention: **verify availability and datasheet revisions before
placing any order** — and per `docs/HANDOFF.md`, don't order fab or parts
without checking with Geoff first.

## Electronics

| Ref | Qty | Part | Package / mount | Why this part | Source |
|---|---|---|---|---|---|
| U1 | 1 | Seeed Studio XIAO RP2040 — **pre-soldered** | Header pins, mounted on carrier BACK via its own presoldered pins pushed through + soldered | [LOCKED] board choice; module carries USB-C, RP2040, flash, NeoPixel | [Seeed, pre-soldered](https://www.seeedstudio.com/Seeed-Studio-XIAO-RP2040-Pre-Soldered-p-6333.html) |
| SW1–SW5 | 5 | Kailh Choc V1 (PG1350) — Brown/tactile suggested | Through-hole switch pins + locating posts | Low-profile mechanical keyswitch: real switch feel in a handheld-thickness shell (11 mm stack vs ~18.5 mm for full MX) | Kailh via distributors (Chosfox, splitkb, MoErgo, AliExpress) |
| — | 5 | MBK Choc-profile 1u keycaps, blank | Friction-fit on Choc stem | Blank per the minimalist/UV-print decision | Same suppliers as switches |
| SW6 | 1 | C&K PCM12SMTR slide switch (SPDT) | Right-angle SMT, actuator past PCB edge | Latch control on the shell *side wall* per §2.3; distinct-by-feel from the keys. Kept SMD — ordinary hand-solder gull-wing pads, not a reflow-only part like the old mic chip, so no reason to swap | [C&K/Littelfuse](https://www.ckswitches.com/products/switches/product-details/Slide/PCM/PCM12SMTR/), Digi-Key `CKN10361CT-ND` |
| MK1 | 1 | I2S MEMS mic **breakout module** (e.g. Adafruit SPH0645, PID 3421) | 6-pin THT header, front side, own onboard acoustic port | Matches the original breadboard-track part (SPEC §7 OQ2) instead of a bare reflow-only chip — hand-solderable header pins | [Adafruit #3421](https://www.adafruit.com/product/3421) |
| D1 | 1 | Plain 3mm THT LED (single color) | THT, front side, top edge | Status LED visible at the top of the shell. Simpler than the old WS2812B: firmware just drives GPIO3 high/low, no bit-banged protocol | Commodity |
| C1 | 1 | 100 nF THT ceramic disc | THT, 5mm lead spacing | Mic VDD decoupling | Commodity |
| C2 | 1 | 100 nF THT ceramic disc | THT, 5mm lead spacing | LED decoupling | Commodity |
| C3 | 1 | 10 µF THT electrolytic/ceramic | THT, 5mm lead spacing | Bulk for LED + mic rail | Commodity |
| R1 | 1 | 300–500 Ω 1/4W axial resistor | THT, formed leads | LED series resistor | Commodity |

Optional (decided against for v2, easy to add later): Kailh Choc hot-swap
sockets (CPG135001S30) — v2 solders switches directly for simplicity and
lower back-side height.

**Superseded from v1** (kept here for history, not for ordering): Knowles
SPH0645LM4H-B bare SMD chip, WS2812B SMD LED, 0603 SMD passives.

## Enclosure hardware

| Qty | Part | Purpose |
|---|---|---|
| 4 | M2 × 16 mm self-tapping screws | Back lid → spacer boss → PCB → front-shell boss (stack now ≈ 2 + 11.5 + 1.6 mm + ~4 mm thread engagement, up from the v1 flush-mount stack — the header-mounted module pushed BACK_GAP out to 11.5mm) |
| 1 | FDM print, 2 parts (front + back shell) | `hardware/enclosure/` outputs |

## Electrical connections (carrier netlist summary)

Pin assignments preserve `docs/SPEC.md` §8 exactly; the only addition is the
status LED on previously-spare D10.

| XIAO pad | GPIO | Net | Connects to |
|---|---|---|---|
| D0 | GPIO26 | `PTT` | SW5 (push-to-talk key) → GND |
| D1 | GPIO27 | `LATCH` | SW6 (slide) common → GND |
| D2 | GPIO28 | `KEY_APPROVE` | SW1 → GND |
| D3 | GPIO29 | `I2S_SD` | MK1 DATA |
| D4 | GPIO6 | `I2S_BCLK` | MK1 BCLK |
| D5 | GPIO7 | `I2S_LRCLK` | MK1 WS/LRCLK |
| D6 | GPIO0 | `KEY_REMEMBER` | SW2 → GND |
| D7 | GPIO1 | `KEY_REJECT` | SW3 → GND |
| D8 | GPIO2 | `KEY_MODE` | SW4 → GND |
| D9 | GPIO4 | spare | — |
| D10 | GPIO3 | `LED_DATA` | R1 → `LED_A` → D1 anode |
| 3V3 | — | `3V3` | MK1 VDD, C1–C3 |
| GND | — | `GND` | all switches, MK1 GND + SEL (left ch.), D1 cathode |

Note on the LED: with a plain THT LED there's no data protocol, just a
GPIO driven high/low through R1 (value depends on the LED's forward
voltage/current — 330Ω is a safe default for a standard red/green 3mm LED
off a 3.3V rail; recompute if a different color/part is picked). All
button/switch inputs use the RP2040 internal pull-ups, active-low, no
external resistors (SPEC §8 convention).
