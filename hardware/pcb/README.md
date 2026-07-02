# Carrier PCB — KiCad project

2-layer carrier board (44 × 104 mm) for the handheld device: hosts the XIAO
RP2040 module (castellated, USB-C at the bottom edge), 5× Kailh Choc V1
keyswitches, the PCM12SMTR side-actuated latch slide, the SPH0645LM4H-B mic
(back side, bottom-port through the board), a WS2812B status LED, and
passives. Net/pin assignments follow `docs/SPEC.md` §8 plus the status LED
on spare D10/GPIO3 — the full netlist table is in `../BOM.md`.

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

1. **XIAO module pads** — check pad width/length/row-spacing against Seeed's
   official footprint (Seeed OPL / wiki KiCad library). Ours: 1.7 × 2.8 mm
   pads, columns at ±8.2 mm, 2.54 mm pitch.
2. **XIAO pin order** — the module is placed USB-down; the pad-to-net map in
   `generate_pcb.py` encodes the 180° rotation of Seeed's USB-up pinout
   drawing. Sanity-check against a physical board before soldering.
3. **PCM12SMTR land pattern** — approximated; pull the real drawing from the
   C&K datasheet.
4. **SPH0645 land pattern** — approximated from the Knowles datasheet; pad
   positions and the 0.7 mm port-hole keepout must match exactly (acoustic
   part, no slop).
5. **Choc contact-pin handedness** — pin 2 at (5.0, −3.8) assumes the common
   variant; check against a physical switch.
6. Run DRC after routing, obviously.

## Coordinate convention

Board space: X = 0 at the board centreline, Y = 0 at the top (mic) edge,
+Y toward the USB-C end. Sheet offset (60, 30) mm. All positions come from
`../design_params.py` — edit there, not here.
