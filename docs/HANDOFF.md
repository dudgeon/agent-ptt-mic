# Handoff — PCB / Industrial Design Track

**Written:** 2026-07-01, end of the requirements-gathering session.
**Why this doc exists:** Geoff asked to hand this specific track (component
selection, physical layout, PCB breakout design, enclosure design, and a
dimensionally accurate 3D mockup) to a more capable model for execution.
This session gathered the requirements and physical/aesthetic decisions;
it deliberately stopped short of doing the design work itself.

## Read first, in this order

1. `docs/SPEC.md` §16 — one paragraph recording that this track was
   explicitly authorized by Geoff ahead of the normal Milestone 7 gate.
2. `docs/PHYSICAL_DESIGN_SPEC.md` — the actual requirements: Geoff's answers,
   the engineering conclusions that follow from them, and section-by-section
   requirements for the PCB, the enclosure, and the 3D mockup. Everything
   below assumes you've read this in full.
3. `docs/SPEC.md` §7, §8, §9, §11 — the original electrical/firmware spec
   (pin map, USB requirements, gating behavior). The custom PCB still needs
   to satisfy all of it; only the *packaging* (SMD parts, carrier board,
   handheld enclosure) is new, not the electrical behavior.

## What's been decided (don't re-ask)

- Handheld remote form factor, cable-tethered, one-hand operation.
- Mechanical keyswitches for the 5 momentary controls (see
  `docs/PHYSICAL_DESIGN_SPEC.md` §2.1 for why low-profile — Kailh Choc or
  Cherry MX Low Profile — is proposed over full-height MX).
- A separate slide/toggle switch for the always-stream latch (§2.2).
- FDM 3D printing as the fabrication target for the enclosure.
- Minimalist, unlabeled surfaces — Geoff will UV-print graphics/labels onto
  the finished case himself. Don't design in engraved or backlit legends.

## What's proposed, not decided (confirm or just proceed and flag again)

- Symmetric/ambidextrous control layout (§2.3) — no handedness preference was
  captured.
- Kailh Choc as the default keyswitch pick over Cherry MX Low Profile — pick
  based on real part availability/footprint-library maturity when you get
  there.
- Bare SPH0645LM4H-B SMD mic placed directly on the carrier PCB, rather than
  the Adafruit breakout used on the separate breadboard track (§2.5).
- Exposing the XIAO module's own USB-C connector through the shell rather
  than adding a second connector to the carrier PCB (§2.4).

If any of these turn out to be wrong once real dimensions/parts are in hand,
that's expected — flag the change rather than silently deviating, same as
the rest of this repo's convention.

## Scoped deliverables for this session

1. **Finalize component part numbers** — keyswitches, latch switch, mic
   (confirm SPH0645LM4H-B is still the right pick or swap it), any
   connectors/hardware needed for the carrier PCB. Update
   `docs/PHYSICAL_DESIGN_SPEC.md` §2 and `docs/SPEC.md` §7 (or add a
   parallel BOM table) with the final picks and links.
2. **PCB breakout design** — a KiCad project (or state your tool choice and
   reasoning if you deviate) implementing `docs/PHYSICAL_DESIGN_SPEC.md` §3:
   XIAO RP2040 module footprint, chosen keyswitch/latch-switch footprints,
   bare mic footprint, 2-layer board, outline coordinated with the enclosure.
   Commit the KiCad project files under `hardware/pcb/`.
3. **Enclosure design** — parametric/code-based CAD (OpenSCAD, CadQuery, or
   build123d strongly preferred — see §4.7's reasoning) implementing
   `docs/PHYSICAL_DESIGN_SPEC.md` §4: split shell, FDM-printable, cutouts for
   USB-C/mic/keyswitches/LED, strain relief, flat UV-print-ready surfaces.
   Commit source + exported STL under `hardware/enclosure/`.
4. **3D mockup** — the assembled device (PCB + components + shell) modeled
   with real component dimensions per `docs/PHYSICAL_DESIGN_SPEC.md` §5, not
   placeholder blocks. Commit under `hardware/mockup/`, and render/export a
   few views (PNG or similar) so Geoff can review without opening a CAD tool.
5. **Update `docs/STATUS.md`** to reflect what got built, and open GitHub
   issues for anything left open (mirroring the existing OQ1–OQ7 pattern in
   issues #1–#10) rather than letting new open questions live only in a
   markdown file.

## Constraints carried over from the rest of the project (still apply)

- No driver install requirement, single USB-C for power+data, continuous
  UAC2 enumeration with firmware-side gating — none of this changes; the PCB
  just needs to physically host the same electrical design.
- Don't start actual PCB fabrication or place a mockup order without
  checking with Geoff first — design and produce files/renders, but treat
  ordering physical parts/prototypes as something to confirm, not assume.
