# Enclosure — FDM-printable handheld shell

Two printed parts (CadQuery source: `enclosure.py`, all dimensions from
`../design_params.py`):

- **Front shell** — front face + full-depth perimeter walls. Openings: one
  shared macropad-style cutout for the 2×2 keystroke cluster, a separate
  framed opening for the PTT key, ⌀1.5 mm mic acoustic hole and ⌀2.5 mm LED
  window at the top, latch-slide slot in the right wall, USB-C opening in
  the bottom wall. Four internal bosses locate and seat the PCB.
- **Back lid** — flush inset panel with four spacer bosses. M2 × 10
  self-tapping screws enter from the back: lid → spacer → PCB → front boss.

Envelope: **49.2 × 109.2 × 14.3 mm** — palm-sized vertical remote. The grip
zone (blank lower third of the front face) is where the XIAO sits inside;
thumb lands on PTT at bottom-centre with the 2×2 cluster above it.

## Regenerating

```
python3 hardware/enclosure/enclosure.py   # writes output/*.stl + *.step
```

`output/` is committed so the parts can be reviewed/printed without running
anything.

## Print notes

- Front shell prints face-down: clean front surface, walls/bosses grow
  upward, no supports; the USB and slide openings in the walls are small
  self-supporting bridges.
- Lid prints flat, boss side up.
- Sharp front edges: the parametric edge-break fillet is currently skipped
  (the CAD kernel refuses the fillet where opening rims meet the corner
  radii — logged at build time). For the fit-check print, break edges in
  the slicer or with sandpaper; a proper chamfer is a v2 modelling task.
- Flat, uninterrupted faces above/below/beside each opening are deliberate:
  they're the UV-print label zones per `docs/PHYSICAL_DESIGN_SPEC.md` §1.

## Fit-check before trusting the model

First print should verify: keycap free travel in the openings (0.5 mm/side
clearance), USB-C plug insertion depth through the 2.6 mm wall, slide-knob
reach through the right wall, and M2 self-tap engagement in the ⌀1.7 pilots.
Adjust `design_params.py` clearances and regenerate rather than editing
geometry by hand.
