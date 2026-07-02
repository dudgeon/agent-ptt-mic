# Status

Live tracker — update this as work happens. `SPEC.md` is the frozen requirements
record; this file is the mutable "where are we right now."

**Last updated:** 2026-07-02

## Current phase

Two concurrent tracks:

1. **Breadboard firmware track (M1–M7, SPEC.md §12).** Pre-hardware-arrival —
   the Seeed Studio XIAO RP2040 has been ordered (see SPEC.md §3, §4) but has
   not arrived. No firmware milestone can be gated/verified on real hardware
   yet (flashing, enumeration checks, audio recording all require the board
   in hand).
2. **PCB / industrial-design track (SPEC.md §16).** Design spike Geoff
   requested while awaiting delivery; runs in parallel with (not instead of)
   the breadboard plan. **First full design pass complete (2026-07-02),
   then revised twice same day:** v2 (Geoff confirmed the XIAO he ordered is
   the **pre-soldered/header SKU** — answers issue #9 ahead of physical
   arrival, still worth a visual check on arrival that it's the RP2040
   family member — and asked to cut unnecessary SMD scope; every active
   part except the LED is now through-hole/header-mount, at the cost of a
   thicker enclosure, ~22.6mm vs. ~14.3mm) and v2.1 (Geoff asked for a true
   RGB status LED; the locked pin map only had 1 spare GPIO after the LED,
   so it reverted to addressable — Geoff confirmed this resolution). See
   `docs/PHYSICAL_DESIGN_SPEC.md` §7 for full rationale and remaining
   deviations awaiting Geoff's confirmation.

   **Two rounds of vendor-cost research done, both from search-snippet
   triangulation only** — this session had no live browser access
   (jlcpcb.com/pcbway.com/most distributor pages 403 every direct fetch).
   That research surfaced a real find (the SW6 latch switch, C&K
   PCM12SMTR, is listed Obsolete) that exposed a bigger gap: **no part in
   `hardware/BOM.md` has been compared against real alternatives** — it's
   explicitly marked provisional now, not final.

   **✅ Live-browser research pass completed 2026-07-02** (handed off
   from the search-snippet session per `docs/HANDOFF.md`). Both scoped
   deliverables done with real browser access, not search snippets:
   - **SW6 component survey (issue #16, flagship task):** live DigiKey/
     Mouser/LCSC parametric search across slide, toggle, rocker, and
     rotary switch categories. **C&K OS102011MA1QN1** (THT right-angle
     slide, $0.66–0.71, confirmed active at 3 independent distributors)
     is the [PROPOSED] leading replacement, with E-Switch EG1218 and a
     CIT toggle switch as alternatives — full comparison table in
     `hardware/BOM.md`. **Not yet Geoff-confirmed** — the pick needs his
     sign-off, and OS102011MA1QN1's body height needs a clearance check
     against `CHOC_H_ABOVE_PCB` before it's final.
   - **Assembly-cost re-verification (issue #15):** live JLCPCB and
     PCBWay instant-quote tools plus JLCPCB's own fee-policy pages.
     Corrected bare-PCB-fab cost sharply downward ($2–6/5 boards at
     JLCPCB, not the $8–20 estimated) and found JLCPCB's overseas
     parts-consignment process is real and documented but carries a flat
     $85 service fee — a genuinely new cost that wasn't priced into the
     old estimates. PCBWay's Combo/Consigned calculator quoted $88
     assembly service for 5 boards. XIAO ($4.90, Seeed direct) and mic
     breakout ($6.95, Adafruit direct, dimensions confirmed
     16.7×12.7×1.8mm) pricing corrected down too. `hardware/BOM.md`,
     `hardware/ASSEMBLY_SOURCING.md`, and `hardware/assembly_options.html`
     all updated with citations; `hardware/design_params.py`'s
     `MIC_BRK_L/W/H` VERIFY tags resolved and PCB/enclosure/mockup
     regenerated (dimensions unchanged in practice — mic breakout size
     doesn't drive `SHELL_T`).

   All decisions from this pass are flagged **[PROPOSED]**, not locked —
   Geoff still needs to confirm the SW6 pick before `slide_pcm12()` and
   the `SLIDE_*` constants get updated. Remaining after that: layout
   sign-off, PCB routing + pre-fab footprint verification, first
   fit-check print.

## Milestone progress (SPEC.md §12)

| Milestone | Gate | Status |
|---|---|---|
| M1 — Toolchain bring-up | Self-built UF2 flashes, LED blinks on custom timing | Not started — blocked on board arrival + OQ1 |
| M2 — HID keyboard standalone | Enumerates as keyboard, zero driver prompts, test keystroke lands | Not started |
| M3 — UAC2 mic standalone (synthetic tone) | Enumerates as audio input, tone recordable | Not started |
| M4 — Composite HID+UAC2 (highest risk) | Single device shows as both, zero drivers | Not started |
| M5 — Real mic integration | Recorded sample is intelligible speech | Not started — blocked on OQ2 (mic purchase) |
| M6 — Buttons/switch/gating/LED | End-to-end test inside real Claude Code session | Not started — blocked on OQ3/OQ4/OQ5 |
| M7 — Polish, freeze for PCB handoff | Pin map/parts/firmware frozen | Not started |

## What can happen before the board arrives

Firmware toolchain setup and skeleton project scaffolding don't require the
physical board — only flashing/testing does. See `firmware/README.md` for
current toolchain status.

## Open questions needing Geoff's input (SPEC.md §5)

- **OQ1** (blocks M1, [#2](https://github.com/dudgeon/agent-ptt-mic/issues/2)):
  toolchain — Pico SDK + TinyUSB vs. Arduino. Proceeding with Pico SDK +
  TinyUSB as the working default per the spec's own recommendation; flag for
  explicit confirmation.
- **OQ2** (blocks M5, [#3](https://github.com/dudgeon/agent-ptt-mic/issues/3)):
  mic part not yet purchased — SPH0645 (Adafruit #3421) recommended.
- **OQ3** (blocks M6, [#4](https://github.com/dudgeon/agent-ptt-mic/issues/4)):
  hardcode default Claude Code keys vs. target a custom `keybindings.json`.
- **OQ4** (blocks M6, [#5](https://github.com/dudgeon/agent-ptt-mic/issues/5)):
  push-to-talk + always-stream both active — proposed always-stream wins.
- **OQ5** (blocks M5/M6, [#6](https://github.com/dudgeon/agent-ptt-mic/issues/6)):
  silence vs. comfort noise when mic gated off.
- **OQ6** (blocks M4, [#7](https://github.com/dudgeon/agent-ptt-mic/issues/7)):
  which OSes need "no driver" validation beyond macOS.
- **OQ7** (non-blocking, [#8](https://github.com/dudgeon/agent-ptt-mic/issues/8)):
  no button for plan-mode's multi-option menu yet.
- **Board arrival checklist** (blocks M1, [#9](https://github.com/dudgeon/agent-ptt-mic/issues/9)):
  confirm SKU/variant the moment the XIAO RP2040 lands.
- **Button-count reconciliation** (blocks M6, [#10](https://github.com/dudgeon/agent-ptt-mic/issues/10)):
  "three buttons" verbatim vs. the 6-control pin map — not yet re-confirmed.

Milestone progress is also tracked as a checklist in
[#1](https://github.com/dudgeon/agent-ptt-mic/issues/1).

## Immediate next steps

### Breadboard track
1. Confirm OQ1 with Geoff (or proceed on the recommended default and flag it).
2. Set up Pico SDK + TinyUSB build environment (does not require the board).
3. When the board arrives: work through SPEC.md §4 / issue #9 (SKU/variant
   check) before anything else.
4. Purchase mic (OQ2) and buttons/switch (SPEC.md §7) — not urgent until M5/M6
   but lead time may be worth ordering now.

### PCB / industrial-design track
1. **Next up — needs Geoff's input:** confirm the SW6 replacement pick
   (issue #16 — survey done 2026-07-02, C&K OS102011MA1QN1 [PROPOSED] as
   leading candidate, see `hardware/BOM.md`) and review the corrected
   assembly-cost figures (issue #15, see `hardware/ASSEMBLY_SOURCING.md`
   and `hardware/assembly_options.html`).
2. Geoff reviews the mockup renders (`hardware/mockup/output/renders/`) and
   confirms/adjusts the layout deviations in `docs/PHYSICAL_DESIGN_SPEC.md`
   §7 (thumb PTT, 2×2 grid, right-side latch) — independent of the SW6
   pick, can happen in parallel.
3. Once SW6 is confirmed: update `slide_pcm12()` in
   `hardware/pcb/generate_pcb.py` and the `SLIDE_*` constants in
   `hardware/design_params.py` to match the chosen part (including a
   body-height clearance check against `CHOC_H_ABOVE_PCB` if
   OS102011MA1QN1 is picked — its THT body may be taller than the SMT
   PCM12SMTR it replaces), then route the carrier board in an interactive
   KiCad session and work the rest of the pre-fab VERIFY list in
   `hardware/pcb/README.md` (mic breakout dimensions already resolved
   this pass; XIAO standoff and Choc pin handedness still need the
   physical parts in hand).
4. FDM fit-check print of the two shell parts (checklist at the end of
   `hardware/enclosure/README.md`). Ordering parts/fab needs Geoff's
   go-ahead first.
