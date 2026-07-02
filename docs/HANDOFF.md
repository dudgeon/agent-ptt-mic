# Handoff — Local Research Agent (Pricing/Sourcing/Component Refinement)

**Status: EXECUTED 2026-07-02.** Both scoped deliverables below (SW6
survey, assembly-cost re-verification) were completed with real browser
access in the local-agent session this handoff was written for. Full
findings are in `hardware/BOM.md` (SW6 comparison table + [PROPOSED]
recommendation), `hardware/ASSEMBLY_SOURCING.md` (live JLCPCB/PCBWay
quotes, new live-verification section at the top), and
`hardware/assembly_options.html` (recomputed cost chart). `docs/STATUS.md`
has the current-state summary. **What's next is not another research
pass — it's Geoff's sign-off** on the SW6 pick (C&K OS102011MA1QN1
[PROPOSED]) before `slide_pcm12()`/`SLIDE_*` get updated and the board
gets routed. The rest of this document is kept for historical context
(the original scoping and "what's already decided" sections are still
accurate) — read `hardware/BOM.md`'s SW6 callout and
`hardware/ASSEMBLY_SOURCING.md`'s live-verification section directly for
the actual findings rather than re-deriving them from the prompt below.

**Written:** 2026-07-02, end of a session that did PCB/enclosure/mockup
design work plus two rounds of vendor-cost research, entirely blocked from
live browser access — direct `WebFetch` of jlcpcb.com, pcbway.com, and
most distributor pages returned HTTP 403 every time, including inside an
automated deep-research workflow (21/21 source fetches failed on the
first attempt). Everything sourcing-related in this repo so far is built
from search-engine-indexed snippets, triangulated across many queries —
real, but weaker evidence than a live page load. **You have real browser
access this session. That's the entire reason for this handoff — use it.**

> ## Prompt used to resume this session
>
> Geoff pastes something close to this to kick off the local agent:
>
> > Continue the `agent-ptt-mic` hardware design track. Read
> > `docs/HANDOFF.md` in full before doing anything else — it has complete
> > context and scoped priorities from the previous session, which had no
> > live browser access (every direct fetch of jlcpcb.com/pcbway.com/
> > distributor pages was blocked). You have real browser access this
> > session — use it to get live quotes, check real stock/pricing, and
> > verify parts/footprints against primary sources instead of search
> > snippets.
> >
> > Priority #1: do a genuine component survey for the always-stream latch
> > switch (SW6). The current pick, C&K PCM12SMTR, is obsolete and was
> > never compared against any alternative — don't assume the SMT-slide-
> > switch category, or the C&K PCM series, is the only viable option.
> > Survey broadly against the actual requirement (see `docs/HANDOFF.md`
> > and `hardware/BOM.md`'s SW6 callout, and GitHub issue #16).
> >
> > Priority #2: re-verify the assembly-cost/sourcing findings in
> > `hardware/ASSEMBLY_SOURCING.md` (GitHub issue #15) with real quotes
> > instead of search snippets.
> >
> > This is a research and refinement pass, not a final-decision pass —
> > leave part/cost decisions open/provisional in the docs (matching the
> > repo's existing **[LOCKED]**/**[PROPOSED]** convention), cite live
> > sources for everything you find, and flag anything that needs Geoff's
> > sign-off rather than deciding for him. Commit and push your findings
> > when done.

## Ground rules

- **Leave decisions open.** `hardware/BOM.md` is explicitly marked
  provisional, not final. Your job is research and refinement: verify
  real prices/stock/footprints, survey alternatives, update docs with
  findings + citations. Don't quietly lock in final part picks — flag
  them for Geoff's confirmation the same way the rest of this repo
  distinguishes **[LOCKED]** from **[PROPOSED]** (see `docs/SPEC.md` §0's
  confidence-label convention, which applies everywhere in this repo).
- **Cite everything.** Every claim you add to `hardware/BOM.md` or
  `hardware/ASSEMBLY_SOURCING.md` should trace to a real URL you actually
  loaded, not a memory or a guess.
- **Don't order anything.** No fab, parts, or PCBA orders without Geoff's
  explicit go-ahead — standing rule, unchanged from every prior handoff
  in this repo.
- **Geoff won't see this session directly** — he's handing this off
  precisely to get a research pass done without spending his own time in
  the loop. Document thoroughly enough that he can review findings
  asynchronously rather than needing to ask you follow-up questions.

## Priority #1: the latch switch (SW6) — deep component survey

**This is the flagship task for this session.** The current pick (C&K
PCM12SMTR) turned out to be listed Obsolete by one distributor — but the
real problem it exposed is that **no alternative was ever surveyed**. Full
context, already written up in detail, is in:

- `hardware/BOM.md` — the expanded "⚠ SW6 (latch switch) — open gap"
  callout: the actual requirement traced to its source (Geoff only ever
  asked for "a switch that makes the mic always stream" — nothing about
  mechanical type, mounting, or manufacturer), what was this session's
  own inference vs. a real requirement, candidate categories nobody has
  compared yet, and filter criteria for a replacement.
- [GitHub issue #16](https://github.com/dudgeon/agent-ptt-mic/issues/16) —
  same content, durable tracking.

Don't just find a replacement part number — use your browser to actually
compare candidates (toggle switches, rocker switches, rotary-detent
switches, other manufacturers' slide switches, possibly a
magnetically-latched slider) against real stock/pricing/datasheets, and
weigh the momentary-button-with-firmware-latch alternative explicitly
(cheaper/simpler, but weakens the physical-state-visibility point behind
`docs/SPEC.md` §3 Locked Decision 6 — worth writing out for Geoff to
weigh in on, not deciding unilaterally). Leave the final pick flagged
**[PROPOSED]** unless Geoff has actually signed off.

## Priority #2: re-verify the v2.1 assembly-cost/sourcing research with real quotes

`hardware/ASSEMBLY_SOURCING.md` and `hardware/assembly_options.html` are
both built from search-snippet triangulation, explicitly caveated as
such. Real next step: get an actual JLCPCB instant quote and an actual
PCBWay quote (their consigned/combo parts flow specifically, per the
current doc's finding that PCBWay is more likely to accept the two
header-mounted modules as customer-supplied parts) using the real files
in this repo (`hardware/pcb/companion_carrier.kicad_pcb`, `hardware/BOM.md`).
Confirm or correct:

- Real PCB fab cost for a 44×104mm 2-layer board at qty 5
- Whether either vendor will actually place the XIAO module and the mic
  breakout module (both header-mounted, not simple components) — this is
  the one thing the previous session flagged as genuinely unconfirmable
  from search snippets alone
- Real per-unit pricing for the XIAO pre-soldered SKU and the mic
  breakout (both had wide, low-confidence price ranges in this round)
- Whether a manual-placement fee for the modules is reasonable or "massive"
  (an EEVblog thread title used exactly that word for a similar case —
  cited as a live warning in `hardware/ASSEMBLY_SOURCING.md`, not
  confirmed against this specific board)

Tracked as [GitHub issue #15](https://github.com/dudgeon/agent-ptt-mic/issues/15).
Update `hardware/assembly_options.html` (mobile-friendly HTML artifact,
built with the repo's `dataviz` skill conventions — see the file itself
for the CSS custom-property palette already in use, reuse it rather than
inventing a new one) once you have real numbers.

## Other open verification items (VERIFY tags scattered across the repo)

Every one of these needs a real datasheet or physical-part check, not
another round of search snippets:

- `hardware/design_params.py`: `XIAO_MODULE_STANDOFF` (header standoff
  gap, currently a typical-for-class estimate), `CHOC_PIN2` (contact pin
  handedness), `MIC_BRK_L`/`MIC_BRK_W` (breakout footprint dimensions),
  `SLIDE_*` constants (tied to SW6 above — will change once a replacement
  is picked).
- `hardware/pcb/generate_pcb.py`: XIAO pad geometry vs. Seeed's official
  footprint, the mic breakout header land pattern, the slide-switch land
  pattern (tied to SW6).
- `hardware/pcb/README.md` "Before fabrication — VERIFY list" — the
  consolidated version of the above, check it against this list for
  drift.

## Read first, in this order

1. This document, in full (you're doing that now).
2. `docs/STATUS.md` — current state of both project tracks (breadboard
   firmware + PCB/industrial-design).
3. `docs/PHYSICAL_DESIGN_SPEC.md` §7 — the full history of the physical
   design revisions (v2: header-mounted XIAO + mic breakout; v2.1: RGB
   LED forced addressable by the pin budget) and why each happened.
4. `hardware/BOM.md` — the provisional parts list, SW6 gap fully written up.
5. `hardware/ASSEMBLY_SOURCING.md` — existing cost/sourcing research,
   including its own "what changed since v1" section and method caveats.
6. `hardware/assembly_options.html` — open this in a real browser; it's
   the cost-comparison artifact Geoff has already seen.
7. GitHub issues #12–#16 — all open, all relevant to this pass.

## What's already decided (don't re-litigate without a real reason)

- Handheld remote form factor, cable-tethered, one-hand operation.
- Kailh Choc V1 low-profile mechanical keyswitches for the 5 momentary
  controls, blank MBK caps.
- XIAO RP2040, **pre-soldered/header SKU** (confirmed by Geoff directly,
  not inferred) — mounts on the carrier's back via its own header pins.
- Mic breakout module (not a bare chip) on the front, matching the
  original breadboard-track part family.
- Addressable RGB status LED — not because it needs to be addressable,
  but because the locked pin map (`docs/SPEC.md` §8) only has 1 spare
  GPIO after accounting for the LED, and discrete RGB needs 3. Geoff
  confirmed this resolution explicitly after being shown the constraint.
- FDM 3D printing as the enclosure fabrication target; minimalist,
  unlabeled surfaces (Geoff UV-prints labels himself post-fab).
- Every active component except the LED is through-hole/header-mount —
  hand-solderable with a plain iron, no reflow/hot-air needed anywhere.

**What's explicitly still open, not just the latch switch:** the whole
BOM is provisional (see the banner at the top of `hardware/BOM.md`).
Don't assume anything in that table is final just because it's written
down — that's exactly the trap SW6 fell into.

## Deliverables for this session — all four completed 2026-07-02

1. ✅ Deep component survey for SW6 (issue #16) with real candidates, real
   pricing/stock, and a clearly-flagged recommendation — not a final
   decision unless Geoff has signed off. **Done:** comparison table in
   `hardware/BOM.md`, C&K OS102011MA1QN1 [PROPOSED] as leading candidate.
2. ✅ Live-quote-verified update to `hardware/ASSEMBLY_SOURCING.md` and
   `hardware/assembly_options.html` (issue #15). **Done:** live JLCPCB/
   PCBWay instant quotes, JLCPCB's real consignment fee schedule, live
   component pricing from Seeed/Adafruit/splitkb.
3. ✅ Resolve as many `VERIFY` tags as practical with real sourced data;
   update `hardware/design_params.py` and regenerate the PCB/enclosure/
   mockup if any dimension changes. **Done:** `MIC_BRK_L/W/H` confirmed
   against Adafruit's own listing and updated; PCB/enclosure/mockup
   regenerated (`python3 hardware/pcb/generate_pcb.py`, `python3
   hardware/enclosure/enclosure.py`, `python3 hardware/mockup/mockup.py
   && python3 hardware/mockup/render.py` — needed `pip install kiutils
   cadquery trimesh` first, none were present in this environment).
   `XIAO_MODULE_STANDOFF` and `CHOC_PIN2` remain open — they genuinely
   need the physical parts in hand, not another search pass. SW6's own
   `SLIDE_*` constants and `slide_pcm12()` footprint are **deliberately
   untouched**, pending Geoff's sign-off on a replacement pick.
4. ✅ Update `docs/STATUS.md` and this document when done, same pattern as
   every prior session in this repo.

## Constraints carried over (still apply, unchanged)

- No driver install requirement, single USB-C for power+data, continuous
  UAC2 enumeration with firmware-side gating — electrical/firmware
  behavior is out of scope for this pass, only sourcing/component
  selection.
- Breadboard firmware track (M1–M7) is a separate, parallel effort — see
  `docs/STATUS.md`. Nothing in this handoff blocks or is blocked by it.

---

## Appendix: prior handoff (executed 2026-07-02, PCB/enclosure/mockup design pass)

<details>
<summary>Original handoff from the requirements-gathering session to the
design-execution session. All five scoped deliverables were completed —
kept here for the record, not as active instructions. Click to expand.</summary>

**Written:** 2026-07-01, end of the requirements-gathering session.
**Why this doc existed:** Geoff asked to hand the PCB/enclosure/mockup
track to a more capable model for execution. That session gathered
requirements and physical/aesthetic decisions; it deliberately stopped
short of doing the design work itself.

### Read first, in this order (original)

1. `docs/SPEC.md` §16 — records that this track was explicitly authorized
   by Geoff ahead of the normal Milestone 7 gate.
2. `docs/PHYSICAL_DESIGN_SPEC.md` — requirements: Geoff's answers, the
   engineering conclusions that follow, section-by-section requirements
   for the PCB, enclosure, and 3D mockup.
3. `docs/SPEC.md` §7, §8, §9, §11 — original electrical/firmware spec.

### What was decided (original)

- Handheld remote form factor, cable-tethered, one-hand operation.
- Mechanical keyswitches for the 5 momentary controls.
- A separate slide/toggle switch for the always-stream latch.
- FDM 3D printing as the fabrication target.
- Minimalist, unlabeled surfaces (UV-print labels post-fab).

### Scoped deliverables (original, all completed)

1. Finalize component part numbers.
2. PCB breakout design (KiCad).
3. Enclosure design (parametric CAD).
4. 3D mockup with real component dimensions.
5. Update `docs/STATUS.md`, open GitHub issues for anything left open.

All five were delivered — see `docs/PHYSICAL_DESIGN_SPEC.md` §7 for the
artifact map, deviations, and the two subsequent same-day revisions
(v2: mounting overhaul; v2.1: RGB LED) this produced.

</details>
