# Bill of Materials — Carrier PCB Track (v2.1)

Final part selections for the custom carrier PCB + handheld enclosure track
(`docs/PHYSICAL_DESIGN_SPEC.md`). The breadboard track's BOM in
`docs/SPEC.md` §7 is separate and unchanged.

**v2 revision (2026-07-02):** the XIAO Geoff actually ordered is the
**pre-soldered/header** SKU (`docs/SPEC.md` §4), not the bare-castellated
one v1 assumed — it mounts via its own presoldered pin headers, not a
flush reflow joint. At the same time, the mic switched from a bare SMD
chip to a breakout module (matching the original breadboard-track part).
Net effect: the XIAO, mic, switches, and passives are all through-hole/
header-mount — hand-solderable with a plain iron, no reflow needed for
any of them — at the cost of a thicker enclosure (~22.6mm vs. ~14.3mm in
v1), since the header-mounted module needs real standoff clearance
instead of sitting flush.

**v2.1 revision (same day):** Geoff asked for the status LED to be RGB.
A genuine discrete RGB LED needs 3 independent GPIOs; the locked pin map
(`docs/SPEC.md` §8) only has 2 spares. Rather than touch the pin map, D1
reverts to an **addressable** RGB LED (WS2812B/SK6812-style) — the only
way to get full RGB from the one GPIO the budget actually has spare.
Firmware only needs to emit solid colors (no animation requirement), but
still has to speak the WS2812 protocol to do that. This is the one
deliberately-reintroduced SMD part on the board — still hand-solderable
(large gull-wing pads, not a reflow-only part like the old mic chip was).

See `hardware/assembly_options.html` for the cost/effort comparison this
enables (**pending a rebuild reflecting v2.1** — see
`docs/PHYSICAL_DESIGN_SPEC.md` §7 for the full rationale on both
revisions).

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
| D1 | 1 | WS2812B (5050) or SK6812 addressable RGB LED | SMD, front side, top edge | v2.1: full RGB "for future status options," reintroduced as addressable because the pin budget only has 1 spare GPIO left (see revision note above) — driven with solid colors only, no animation requirement | Commodity |
| C1 | 1 | 100 nF THT ceramic disc | THT, 5mm lead spacing | Mic VDD decoupling | Commodity |
| C2 | 1 | 100 nF THT ceramic disc | THT, 5mm lead spacing | LED decoupling | Commodity |
| C3 | 1 | 10 µF THT electrolytic/ceramic | THT, 5mm lead spacing | Bulk for LED + mic rail | Commodity |
| R1 | 1 | 300–500 Ω 1/4W axial resistor | THT, formed leads | LED data-line series resistor (signal integrity, not current-limiting — WS2812 draws its own current) | Commodity |

Optional (decided against for v2, easy to add later): Kailh Choc hot-swap
sockets (CPG135001S30) — v2 solders switches directly for simplicity and
lower back-side height.

**Superseded from v1** (kept here for history, not for ordering): Knowles
SPH0645LM4H-B bare SMD chip, 0603 SMD passives.
**Superseded from v2** (briefly, same day): plain 3mm THT LED — reverted
to addressable in v2.1 per the pin-budget constraint above.

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
| D10 | GPIO3 | `LED_DATA` | R1 → `LED_DIN` → D1 DIN |
| 3V3 | — | `3V3` | MK1 VDD, D1 VDD, C1–C3 |
| GND | — | `GND` | all switches, MK1 GND + SEL (left ch.), D1 GND |

Note on the LED (v2.1): D1 is addressable (WS2812B/SK6812-style), so
GPIO3 carries the WS2812 single-wire data protocol through R1 to DIN, not
a simple high/low current-limited drive. D1's DOUT is left unconnected
(not chained to a second LED). WS2812B is a 5V part that generally runs
fine at 3.3V with a 3.3V data signal; swap to SK6812 (native 3.3V) if
brightness/reliability disappoints. All button/switch inputs use the
RP2040 internal pull-ups, active-low, no external resistors (SPEC §8
convention).
