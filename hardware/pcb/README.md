# Carrier PCB — KiCad project

2-layer carrier board (44 × 104 mm) for the handheld device: hosts the XIAO
RP2040 module (**pre-soldered/header SKU**, mounted on the BACK via its own
header pins, USB-C facing away into the back shell), 5× Kailh Choc V1
keyswitches, the PCM12SMTR side-actuated latch slide, an I2S mic
**breakout module** (front side, THT header), an **addressable RGB LED**
(WS2812B/SK6812-style — the one deliberately-reintroduced SMD part, see
below) + THT passives — every other active part is through-hole/header-
mount, hand-solderable with a plain iron (2026-07-02 revision; see
`docs/PHYSICAL_DESIGN_SPEC.md` §7 for why). Net/pin assignments follow
`docs/SPEC.md` §8 plus the status LED on spare D10/GPIO3 — the full
netlist table is in `../BOM.md`.

**Why the LED is SMD again:** Geoff asked for a true RGB status LED. A
discrete (non-addressable) RGB LED needs 3 independent GPIOs; the locked
pin map only has 2 spares. An addressable LED needs just 1 data pin, so
it's the only option that fits — still hand-solderable (large gull-wing
pads), just not through-hole.

## Files

- `generate_pcb.py` — the source of truth. Regenerates the board file from
  `../design_params.py`. Run `python3 hardware/pcb/generate_pcb.py` from the
  repo root after changing any dimension or position.
- `companion_carrier.kicad_pcb` — generated output (committed so it can be
  reviewed/opened without running anything).
- `companion_carrier.kicad_pro` — project file.

## Status: placed + netlisted, NOT routed

Deliberate scope cut, not an oversight: every footprint is placed and every
pad carries its net (open the board in KiCad and the full ratsnest appears),
but copper traces are not laid. Hand-computing trace geometry outside KiCad
means no live DRC, which is how you ship shorts. Routing this board in an
interactive KiCad session is ~30 minutes of work: all signals are slow
single-ended GPIO, the only mild care point is keeping the three I2S lines
short-ish and away from the LED data line. GND zones on both layers are
declared (fill them with `B` in pcbnew).

There is intentionally no `.kicad_sch`: the circuit is 17 components with a
one-net-per-switch topology, fully specified by the netlist table in
`../BOM.md` and encoded on the pads here. Drawing a schematic in KiCad from
that table is mechanical; hand-writing `.kicad_sch` s-expressions without
KiCad available to validate them is where errors would creep in.

## Before fabrication — VERIFY list

Footprint geometry here is derived from datasheets/community footprints at
design time. Before generating gerbers:

1. **XIAO header pin holes** — drill/pad size (currently 1.0mm drill,
   1.8mm pad) must fit the actual presoldered pin diameter; check against
   the physical board, not just a generic 0.1" header assumption.
2. **XIAO pin order** — the module is placed USB-down, back side; the
   pad-to-net map in `generate_pcb.py` encodes the 180° rotation of
   Seeed's USB-up pinout drawing. Sanity-check against a physical board
   before soldering.
3. **XIAO standoff/pin length** — `design_params.py XIAO_MODULE_STANDOFF`
   (6.0mm) is an estimate for how far the module hangs off the carrier;
   measure the real pin length before finalizing the enclosure thickness.
4. **SW6 land pattern (`slide_pcm12()`)** — still the PCM12SMTR footprint.
   A deep component survey (2026-07-02, issue #16, see `../BOM.md`) found
   C&K OS102011MA1QN1 as the leading [PROPOSED] replacement — pending
   Geoff's sign-off. Once a pick is confirmed, this footprint (and the
   `SLIDE_*` constants in `design_params.py`) need updating — not done
   yet, deliberately, per the issue's scope boundary.
5. **Mic breakout footprint** — `MIC_BRK_L`/`MIC_BRK_W`/`MIC_BRK_H`
   **confirmed 2026-07-02** against Adafruit's own listing for #3421
   (16.7 × 12.7 × 1.8mm) — no longer an estimate, `design_params.py`
   updated. Pin pitch (2.54mm, 6-pin header) still assumed standard —
   worth a quick physical check but low risk.
6. **Choc contact-pin handedness** — pin 2 at (5.0, −3.8) assumes the common
   variant; check against a physical switch.
7. Run DRC after routing, obviously.

## Coordinate convention

Board space: X = 0 at the board centreline, Y = 0 at the top (mic) edge,
+Y toward the USB-C end. Sheet offset (60, 30) mm. All positions come from
`../design_params.py` — edit there, not here.
