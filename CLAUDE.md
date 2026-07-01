# Claude Code Companion Peripheral

Hardware/firmware project: a Seeed Studio XIAO RP2040 that enumerates as a
composite USB device (HID keyboard + USB Audio Class microphone, no drivers)
with physical buttons for push-to-talk, always-on mic latch, and Claude Code
approval-prompt keystrokes.

## Before doing anything

1. Read `docs/SPEC.md` in full — it is the single source of truth, derived
   from the project owner's (Geoff's) own words, and there is no other
   record of these requirements. Sections 3–5 (locked decisions, board
   arrival checklist, open questions) matter most.
2. Read `docs/STATUS.md` for current progress and what's blocked on what.
3. Respect the confidence labels in the spec:
   - **[LOCKED]** — do not revisit without asking Geoff.
   - **[PROPOSED]** — working default; flag back to Geoff at the next
     natural checkpoint rather than treating it as settled.
   - **[OPEN]** — a real unresolved decision; check `docs/STATUS.md` and the
     repo's issues for the current state before assuming an answer.

## Hard constraints (do not relitigate)

- Board is the Seeed Studio XIAO RP2040 — already ordered, choice is final.
- No driver install, ever, on any target OS (HID + USB Audio Class only).
- Single USB-C connector for power and data — bus-powered, no battery.
- Mic USB interface stays enumerated continuously; push-to-talk/always-stream
  gate real-vs-silence samples in firmware, not by re-enumerating USB.
- Breadboard first; no custom PCB work until the Milestone 7 gate in
  `docs/SPEC.md` §12 is met and Geoff explicitly asks for it. **Exception:**
  Geoff explicitly asked to start a concurrent PCB/enclosure track on
  2026-07-01 — see `docs/SPEC.md` §16 and `docs/PHYSICAL_DESIGN_SPEC.md`.
  This does not cancel the breadboard plan; both tracks run in parallel.

## Work plan

Follow the milestone sequence in `docs/SPEC.md` §12 (M1–M7) in order. Each
milestone has a hard pass/fail gate — don't skip ahead. M4 (composite
HID+UAC2 descriptor) is the highest-risk step in the project.

## Repo layout

- `docs/SPEC.md` — frozen requirements spec (do not edit except to correct
  factual errors or record an explicit decision from Geoff).
- `docs/STATUS.md` — live/mutable progress tracker; update as work happens.
- `docs/PHYSICAL_DESIGN_SPEC.md` — requirements for the concurrent PCB /
  enclosure / 3D-mockup track (component selection, physical layout, PCB and
  enclosure requirements — not yet a finished design).
- `docs/HANDOFF.md` — scoped deliverables for the next session on the PCB /
  industrial-design track.
- `firmware/` — RP2040 firmware (Pico SDK + TinyUSB, per OQ1's recommended
  default).
- `hardware/` — BOM, wiring/pin notes, breadboard photos/notes.
