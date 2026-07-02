# Bill of Materials — Carrier PCB Track (v1)

Final part selections for the custom carrier PCB + handheld enclosure track
(`docs/PHYSICAL_DESIGN_SPEC.md`). The breadboard track's BOM in
`docs/SPEC.md` §7 is separate and unchanged.

Per project convention: **verify availability and datasheet revisions before
placing any order** — and per `docs/HANDOFF.md`, don't order fab or parts
without checking with Geoff first.

## Electronics

| Ref | Qty | Part | Package / mount | Why this part | Source |
|---|---|---|---|---|---|
| U1 | 1 | Seeed Studio XIAO RP2040 | Castellated module, reflow/hand-solder onto carrier | [LOCKED] board choice; module carries USB-C, RP2040, flash, NeoPixel | [Seeed](https://www.seeedstudio.com/XIAO-RP2040-v1-0-p-5026.html) |
| SW1–SW5 | 5 | Kailh Choc V1 (PG1350) — Brown/tactile suggested | Through-hole switch pins + locating posts | Low-profile mechanical keyswitch: real switch feel in a handheld-thickness shell (11 mm stack vs ~18.5 mm for full MX) | Kailh via distributors (Chosfox, splitkb, MoErgo, AliExpress) |
| — | 5 | MBK Choc-profile 1u keycaps, blank | Friction-fit on Choc stem | Blank per the minimalist/UV-print decision | Same suppliers as switches |
| SW6 | 1 | C&K PCM12SMTR slide switch (SPDT) | Right-angle SMT, actuator past PCB edge | Latch control on the shell *side wall* per §2.3; distinct-by-feel from the keys | [C&K/Littelfuse](https://www.ckswitches.com/products/switches/product-details/Slide/PCM/PCM12SMTR/), Digi-Key `CKN10361CT-ND` |
| MK1 | 1 | Knowles SPH0645LM4H-B I2S MEMS mic | SMD, bottom-port, back side of PCB | Same mic family as OQ2's pick, as the bare part per §2.5 | Digi-Key `423-1405-1-ND`, Mouser |
| D1 | 1 | WS2812B (5050) addressable RGB LED | SMD, front side, top edge | Status LED visible at the top of the shell; XIAO's own NeoPixel sits at the bottom under the shell, so a carrier LED on spare GPIO3/D10 replaces it | Commodity |
| C1 | 1 | 100 nF X7R 0603 | SMD | Mic VDD decoupling | Commodity |
| C2 | 1 | 100 nF X7R 0603 | SMD | LED decoupling | Commodity |
| C3 | 1 | 10 µF X5R 0805 | SMD | Bulk for LED + mic rail | Commodity |
| R1 | 1 | 300–500 Ω 0603 | SMD | WS2812 data-line series resistor | Commodity |

Optional (decided against for v1, easy to add later): Kailh Choc hot-swap
sockets (CPG135001S30) — v1 solders switches directly for simplicity and
lower back-side height.

## Enclosure hardware

| Qty | Part | Purpose |
|---|---|---|
| 4 | M2 × 10 mm self-tapping screws | Back lid → spacer boss → PCB → front-shell boss (stack ≈ 2 + 3.2 + 1.6 mm + ~4 mm thread engagement) |
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
| D10 | GPIO3 | `LED_DATA` | R1 → D1 DIN |
| 3V3 | — | `3V3` | MK1 VDD, D1 VDD (see note), C1–C3 |
| GND | — | `GND` | all switches, MK1 GND + SEL (left ch.), D1 GND |

Note on the LED rail: WS2812B is a 5 V part that generally runs fine at
3.3 V with a 3.3 V data signal (VDD ≈ VDATA keeps logic thresholds valid).
If brightness/reliability disappoints, swap D1 to an SK6812 (3.3 V-happy)
or feed it from the XIAO's 5 V VBUS pad — both are drop-in at this layout.
All button/switch inputs use the RP2040 internal pull-ups, active-low, no
external resistors (SPEC §8 convention).
