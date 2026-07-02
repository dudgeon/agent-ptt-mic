# Carrier PCB — KiCad project

2-layer carrier board (44 × 104 mm) for the handheld device: hosts the XIAO
RP2040 module (**pre-soldered/header SKU**, mounted on the BACK via its own
header pins, USB-C facing away into the back shell), 5× Kailh Choc V1
keyswitches, the **C&K OS102011MA1QN1** side-actuated latch slide (THT,
right-angle — replaced the obsolete PCM12SMTR, issue #16), an I2S mic
**breakout module** (front side, THT header), an **addressable RGB LED**
(WS2812B/SK6812-style — the one deliberately-reintroduced SMD part, see
below) + THT passives — every other active part is through-hole/header-
mount, hand-solderable with a plain iron (2026-07-02 revision; see
`docs/PHYSICAL_DESIGN_SPEC.md` §7 for why). Net/pin assignments follow
`docs/SPEC.md` §8 plus the status LED on spare D10/GPIO3 — the full
netlist table is in `../BOM.md`. Front silkscreen carries
`agent-ptt-mic-v0 / Geoff Dudgeon & Claude` (Geoff's request, 2026-07-02).

**Why the LED is SMD again:** Geoff asked for a true RGB status LED. A
discrete (non-addressable) RGB LED needs 3 independent GPIOs; the locked
pin map only has 2 spares. An addressable LED needs just 1 data pin, so
it's the only option that fits — still hand-solderable (large gull-wing
pads), just not through-hole.

## Files

- `generate_pcb.py` — the source of truth for placement + netlist.
  Regenerates the board file from `../design_params.py`. Run
  `python3 hardware/pcb/generate_pcb.py` from the repo root after changing
  any dimension or position — **then re-run the routing pipeline below**
  (regenerating discards routing).
- `route_board.py` — step 2: headless routing via freerouting + zone fill.
  Needs KiCad's bundled python (for `pcbnew`) and a freerouting jar; see
  its docstring for exact invocation.
- `companion_carrier.kicad_pcb` — generated, **routed** output (committed).
- `companion_carrier.kicad_pro` — project file.
- `fab/companion_carrier_v0_gerbers.zip` — Gerbers + Excellon drill files,
  ready for JLCPCB/PCBWay upload.
- `fab/companion_carrier-cpl.csv` — component placement (pos) file for
  PCBA quoting.
- `fab/board_top.png`, `fab/board_bottom.png` — 3D renders of the routed
  board (`kicad-cli pcb render`).

## Status: ROUTED, DRC-clean (2026-07-02)

Routed headlessly with KiCad 10.0.4 + freerouting 2.2.4 (the repo's old
"route interactively" rule was about having real DRC, not about hands on
a mouse — this pipeline runs KiCad's own DRC):

```
python3 hardware/pcb/generate_pcb.py
<kicad-python> hardware/pcb/route_board.py <freerouting.jar>
kicad-cli pcb drc --severity-error --exit-code-violations ...
kicad-cli pcb export gerbers/drill/pos ...
```

Final DRC: **0 error-severity violations, 0 unconnected items.** Remaining
warnings are cosmetic (silk-over-copper clips at fab, generated footprints
aren't from a library, two unmirrored back-silk ref texts). Two real
issues were caught and fixed by the first DRC run: R1's +X pad landed on
SW6's pin 1 (R1 moved to x=8), and SW6's support-leg pads sat 0.25mm from
the board edge (moved to the footprint centreline). SW5's GND pad uses a
solid zone connection instead of thermal spokes — the PTT switch's
stem/post holes crowd the F.Cu zone below the 2-spoke DRC minimum.

There is intentionally no `.kicad_sch`: the circuit is 17 components with a
one-net-per-switch topology, fully specified by the netlist table in
`../BOM.md` and encoded on the pads here. Drawing a schematic in KiCad from
that table is mechanical; hand-writing `.kicad_sch` s-expressions without
KiCad available to validate them is where errors would creep in.

## Before ordering fabrication — VERIFY list

Gerbers exist and DRC is clean, but footprint geometry is still
datasheet-derived. Before actually placing a fab order, check against
physical parts:

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
4. **SW6 land pattern (`slide_os102()`)** — C&K OS102011MA1QN1, pin/
   support-hole pattern from the OS series datasheet (3× ø0.8 @ 2.1mm +
   2× ø1.5 @ 8.2mm span). The pin row's exact X offset within the body
   and the support-leg offset were read off the drawing at print
   precision — measure a physical part before ordering.
5. **Mic breakout footprint** — `MIC_BRK_L`/`MIC_BRK_W`/`MIC_BRK_H`
   **confirmed 2026-07-02** against Adafruit's own listing for #3421
   (16.7 × 12.7 × 1.8mm) — no longer an estimate, `design_params.py`
   updated. Pin pitch (2.54mm, 6-pin header) still assumed standard —
   worth a quick physical check but low risk.
6. **Choc contact-pin handedness** — pin 2 at (5.0, −3.8) assumes the common
   variant; check against a physical switch.
7. Re-run the route pipeline + DRC after any of the above change a
   dimension (regeneration discards routing — `route_board.py` re-routes
   in seconds).

## Coordinate convention

Board space: X = 0 at the board centreline, Y = 0 at the top (mic) edge,
+Y toward the USB-C end. Sheet offset (60, 30) mm. All positions come from
`../design_params.py` — edit there, not here.
