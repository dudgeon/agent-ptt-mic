# Physical Design Spec — PCB Breakout, Enclosure, and 3D Mockup

**Status:** Requirements captured, design work not yet started.
**Scope note:** This track was explicitly requested by Geoff ahead of the
`docs/SPEC.md` §12 Milestone 7 gate ("no PCB work until the breadboard design
is functionally locked"). Per that document's own tie-breaker rule — a direct
instruction from Geoff overrides a locked decision — this is intentional and
tracked here rather than silently overriding §3.4. The breadboard milestone
plan (M1–M6) is unaffected and continues in parallel; this document covers a
second, concurrent track: selecting exact components and designing the
custom carrier PCB + handheld enclosure + a dimensionally-accurate 3D mockup.

This document is the handoff input for that second track. It captures the
decisions gathered directly from Geoff plus the engineering conclusions that
follow from them. **It does not contain finished component picks, PCB
layout, or 3D files** — those are the next session's deliverables (see
`docs/HANDOFF.md`).

---

## 1. Decisions gathered from Geoff (this session)

| Question | Answer |
|---|---|
| Form factor / mounting | **Handheld remote** — small enough to hold in one hand like a clicker, cable-tethered (not a desk puck, not keyboard/monitor-mounted). |
| Button tactile feel | **Mechanical keyswitches** — real switch mechanism with removable keycaps, not membrane/rubber-dome or bare SMD tactile buttons. |
| Enclosure fabrication | **3D printed, FDM** — desktop/service FDM printing, not resin/SLA, not laser-cut, not an off-the-shelf box. |
| Aesthetic / legends | **Minimalist** — clean, unlabeled surfaces. Geoff intends to add labels/graphics himself via **UV printing** onto the finished case after fabrication. The enclosure design must therefore leave flat, uninterrupted print-friendly surfaces near each control rather than integrating engraved/backlit legends. |

---

## 2. Engineering implications and proposed follow-ons [PROPOSED — confirm during next session or at the next checkpoint with Geoff]

These follow directly from the answers above but weren't asked explicitly —
flagging each rather than silently deciding.

### 2.1 Mechanical keyswitches in a handheld form factor → low-profile switch family
A **full-height Cherry MX-style switch** (~11mm switch body + ~7–8mm keycap
≈ 18–20mm stack height) makes for a thick, chunky handheld object — closer to
a game controller than a clicker. Given "handheld remote" was the explicit
form-factor choice, **low-profile mechanical switches** better satisfy both
answers at once:
- **Kailh Choc (PG1350, V1)** — ~11mm × 13.8mm footprint, ~2.6mm actuation
  travel, low-profile keycaps available (Choc/MBK caps), hot-swap sockets
  exist. Widely used in slim mechanical keyboards; well-documented KiCad
  footprints exist in community libraries.
- **Cherry MX Low Profile (RGB / Speed)** — same MX-compatible mount pattern
  as standard MX but ~11.9mm total height instead of ~18mm+; standard MX
  low-profile keycaps required (not interchangeable with full MX caps).
- **Recommendation for next session:** default to Kailh Choc V1 unless the
  next session's part-availability check favors Cherry MX Low Profile —
  Choc has the smaller footprint of the two, which matters more for a
  one-hand device.

### 2.2 The always-stream latch is a different control class than the 5 momentary buttons
A latching "always-stream" control shouldn't use a momentary keyswitch (it
would need firmware-side toggle logic and risks feeling wrong under the
thumb). Propose a small **mechanical slide or toggle switch** (e.g. C&K
sub-mini slide switch, or E-Switch EG-series toggle) as a genuinely distinct
part and physical affordance from the 5 keyswitches — so it's
unmistakable by feel alone which control is the latch.

### 2.3 Proposed control layout (handheld, one-hand operation)
No handedness preference was captured — proposing a **symmetric/ambidextrous**
layout as the default; flag for confirmation once a hand-sized mockup exists
and can be test-gripped.

- **Front face (thumb cluster):** the 4 keystroke buttons (Approve /
  Approve+Remember / Reject / Mode-toggle) arranged in a diamond, similar to
  a game-controller face-button cluster — reachable by thumb without
  regripping.
- **Top edge (index-finger position):** push-to-talk as a trigger/bumper-style
  control — distinct motion (squeeze vs. thumb-press) reduces the chance of
  confusing it with the keystroke buttons under stress.
- **Side of the shell:** the always-stream latch switch, positioned off the
  primary grip line to reduce accidental toggling.
- **Bottom edge:** USB-C cable exit + strain relief, so the cable trails away
  from the hand naturally during use.
- **Status LED:** the XIAO's onboard NeoPixel, either exposed directly at the
  top of the shell or routed to the surface via a small light pipe — final
  approach depends on where the module ends up sitting inside the shell.

### 2.4 USB-C: reuse the XIAO module's own connector, don't add a second one
The XIAO RP2040 module already has a USB-C connector on it. Recommend
mounting the module at the shell's edge so **its own connector is exposed
through a single cutout**, rather than adding a second USB-C connector to
the carrier PCB and re-routing D+/D− across a board-to-board connection —
simpler and removes a class of signal-integrity risk for no benefit here.

### 2.5 Microphone: place the bare SMD part on the carrier PCB, not a breakout module
`docs/SPEC.md` OQ2 recommends the SPH0645LM4H as a breakout board (Adafruit
#3421) for the breadboard track, which is still correct for M5. For the
custom-PCB track, since we're now doing SMD placement anyway, recommend
laying out the **bare SPH0645LM4H-B SMD MEMS mic package directly on the
carrier PCB** instead of mounting a separate breakout — matches the "PCB
breakout board that will take the SMD components" framing of this request.
This requires the enclosure's sound port hole to align to wherever the
carrier PCB places the mic (top-port vs. bottom-port orientation must be
confirmed against the current SPH0645LM4H datasheet next session — Adafruit's
breakout silkscreen is not a reliable substitute for the bare-part datasheet
here).

---

## 3. PCB breakout board — requirements for next session

1. **Carries the XIAO RP2040 module directly**, soldered via its castellated
   edge pads (per `docs/SPEC.md` §14 — the module is designed to be
   reflow/hand-soldered onto a carrier, no components populated on its
   underside). Source the module's real footprint from Seeed's official
   KiCad/Eagle library rather than hand-deriving pad positions from the wiki
   pinout diagram.
2. **Board outline is driven by the enclosure**, not the other way around —
   the handheld shell's internal cavity (from Section 4 below) sets the PCB's
   maximum size, not vice versa.
3. **2-layer PCB** is very likely sufficient — no high-speed routing beyond
   what the XIAO module already handles internally; carrier traces are just
   GPIO-to-switch and GPIO/PIO-to-mic.
4. **Switch footprints:** source real KiCad footprints for the chosen
   keyswitch family (Section 2.1) and the latch switch (Section 2.2) from
   community or manufacturer libraries — don't hand-derive from datasheet
   dimensions if a verified footprint already exists.
5. **Mic:** bare SPH0645LM4H-B SMD footprint per Section 2.5, oriented to
   match the enclosure sound port.
6. **Mounting:** holes/standoff positions matched to the enclosure design
   (Section 4) — coordinate the two designs together rather than sequentially.
7. **Design tool:** not yet chosen — recommend KiCad (free, scriptable,
   widely supported footprint libraries) unless the next session has a
   reason to prefer something else.

---

## 4. Enclosure — requirements for next session

1. **Form factor:** handheld remote, roughly clicker/game-controller sized —
   final dimensions driven by the keyswitch cluster footprint (2.1, 2.3) plus
   hand-fit margin, not chosen independently.
2. **Fabrication target: FDM 3D printing.** Design with FDM constraints in
   mind: minimum wall thickness for the printer/material in use (verify, but
   ~1.5–2mm is a reasonable starting assumption), avoid unsupported overhangs
   beyond ~45°, avoid features that require supports inside tight cavities
   (e.g., the switch/keycap openings).
3. **Split-shell design** (top/bottom halves, screwed or snap-fit together)
   for printability and access to the PCB/wiring — a one-piece shell isn't
   FDM-friendly for something this complex.
4. **Surfaces left flat and unadorned** near each control, sized to
   accommodate UV-printed labels/graphics added after fabrication (Section 1)
   — no engraved or backlit legends designed in.
5. **Cutouts:** USB-C connector (Section 2.4), mic sound port (Section 2.5),
   keyswitch openings sized to the chosen switch/keycap family, status LED
   window or light pipe.
6. **Strain relief** at the cable exit point.
7. **Deliverable format:** parametric/code-based CAD (OpenSCAD, CadQuery, or
   build123d) is strongly preferred over a GUI-only tool — it's versionable
   in this repo and an agent can iterate on it directly. STL for
   print-testing, STEP if a GUI tool is used for any part of the process.

---

## 5. 3D mockup — requirements for next session

The mockup must be **dimensionally accurate to the actual selected
components**, not placeholder blocks:
- Real XIAO RP2040 module footprint and height (including USB-C connector
  position on the module itself).
- Real keyswitch body dimensions and keycap profile for whichever family is
  selected (2.1).
- Real latch switch dimensions (2.2).
- Real SPH0645LM4H-B package dimensions and port location (2.5).
- Carrier PCB thickness (standard 1.6mm unless a reason emerges to change it).

Pull every dimension from the current datasheet/footprint library for the
part actually selected — do not carry forward a dimension from an earlier
guess without re-checking it against source data, since component picks in
Section 2 are proposals, not final.

---

## 6. What this document deliberately does not do

- Does not pick final manufacturer/part numbers — Section 2 lists candidate
  families, not a locked BOM.
- Does not produce KiCad schematic/PCB files, CAD files, or STL/STEP output.
- Does not change the breadboard-track BOM in `docs/SPEC.md` §7 or the M1–M7
  milestone plan — those continue independently on the original hardware
  (Adafruit SPH0645 breakout, no custom PCB) until the M7 gate.
