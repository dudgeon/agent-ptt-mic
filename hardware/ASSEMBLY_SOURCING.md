# Assembly sourcing — JLCPCB vs PCBWay (zero-solder feasibility)

**Current as of:** 2026-07-02, v2.1 BOM (pre-soldered/header XIAO, mic
breakout module, addressable RGB LED — see `hardware/BOM.md`). Supersedes
the v1 research kept as an appendix at the bottom of this file.

**Method note, both rounds:** direct `WebFetch` of jlcpcb.com and
pcbway.com pages returns HTTP 403 (bot-blocked) every time, including
inside the automated deep-research workflow (21/21 sources failed there
on the first pass). This round is built from ~14 targeted `WebSearch`
queries against search-engine-indexed snippets — including community/
forum sources (EEVblog, Deskthority, Hackaday.io) alongside vendor pages
— triangulated across independent queries per claim. Treat anything not
phrased as "confirmed" as needing a live quote-tool check, not settled
fact.

## What changed since the v1 research

The v1 BOM had a bare SMD mic chip and a single-color LED — nothing that
looked like a genuine "module." The v2.1 BOM has **two actual modules**
sitting on header pins (the XIAO itself, and the mic breakout), and
that's a fundamentally different sourcing question than "is this
component in a vendor's parts library" — assembly houses' pick-and-place
equipment is built to place discrete components fed from tape/reel/tray,
not whole daughterboard modules standing off on their own header pins.
That reframes the whole "zero solder" question.

## Headline finding: JLCPCB vs. PCBWay diverge on customer-supplied parts

- **JLCPCB:** "generally does not accept customer-supplied components for
  their standard assembly service, to maintain quality control and
  component traceability." Their help-center consignment articles
  (`how-to-consign-parts-to-jlcpcb`, `consignment-part-terms-conditions`)
  exist, but read as a separate, more manual process — not part of the
  self-service instant-quote flow most small orders use.
- **PCBWay:** explicitly supports **Kitted/Consigned** (customer supplies
  all parts) and **Combo** (customer supplies some, PCBWay sources the
  rest) as first-class order types, with published rules for how
  customer-supplied parts must be packaged (reeled/taped, minimum
  quantities per package type).

**This flips last round's lean.** With a BOM that's mostly discrete
components, JLCPCB's "everything's already in our library" story won out.
With two actual modules that need to be supplied by the customer either
way, PCBWay's willingness to accept consigned parts as a matter of
routine process is the more relevant capability — *if* an assembly
house's manual-placement fee for something as tall/irregular as these
modules doesn't erase the benefit (see the EEVblog "massive manual
assembly fee" thread referenced in the Q&A below; nobody should assume
this is cheap without a real quote).

## Q&A summary (v2.1 BOM)

1. **Can either vendor place the XIAO or the mic breakout module?**
   Uncertain, and this is the crux of the whole question. JLCPCB's
   standard flow likely declines (no customer-supplied parts outside
   their library). PCBWay's consigned/combo flow is built for exactly
   this case in principle, but a header-pin module standing several mm
   off the board is still an irregular-placement item — JLCPCB's own
   fee schedule for "components that cannot be picked up by machines"
   ($0.0157/pin manual-placement fee, "may increase if difficult") shows
   this class of part is treated as an exception even when accepted, not
   routine. Needs a real quote from PCBWay to know if they'll even take
   the job, and at what fee.
2. **THT soldering (switches, passives).** Both vendors offer wave/
   selective-soldering for through-hole parts as a paid add-on
   (JLCPCB: ~$3.50 flat hand-soldering labor + ~$0.0135–0.0173/joint) —
   this part of the finding is unchanged from v1 and still solid: the 5
   keyswitches, the passives, and (if a replacement part is picked, see
   below) the latch switch are all ordinary vendor-assemblable work.
3. **LED in-library:** WS2812B confirmed cheap and widely stocked —
   LCSC lists Worldsemi WS2812B variants at $0.03–0.05/unit in reel
   quantities; expect more like $0.30–0.60/unit for small hobbyist
   quantities from Amazon/AliExpress-style sellers.
4. **Part risk found this round, not previously flagged:** the C&K
   PCM12SMTR slide switch (SW6, the latch) is listed **Obsolete** by
   Future Electronics. DigiKey/RS Online/LCSC still show it orderable at
   this writing, but it's not a part to build a long-term footprint
   around — tracked as issue #16.
5. **MOQ/pricing, updated for this board's real footprint:** the carrier
   is 44×104mm — over JLCPCB's "$2-for-5-boards under 100×100mm" bracket
   (104mm exceeds the 100mm side), so PCB fab alone likely runs
   somewhere in the $8–20/5-boards range rather than the headline $2,
   though an exact figure needs the live quote tool. PCBA setup+stencil
   minimums cluster around $30–70 for a double-sided board at JLCPCB
   (one referenced July-2025 example: $33.66 minimum for single-sided
   Economic PCBA setup+stencil alone, before parts/labor). PCBWay's
   often-cited "$5 for 5-10 boards" figure is PCB fab only, not PCBA —
   don't conflate the two when reading vendor marketing pages.
6. **Whole-device, one vendor:** unchanged from v1 — JLCPCB+JLC3DP have a
   documented combined-order flow; PCBWay offers the same service breadth
   but combined ordering leans on contacting their sales team.
7. **Updated small-parts pricing (informs the cost artifact):**
   - XIAO RP2040, pre-soldered: ~£19 (~$24) at UK retail (Amazon.co.uk);
     US pricing likely somewhat lower direct from Seeed — verify before
     ordering, regional/retailer price spread is wide for this part.
   - Mic breakout (Adafruit SPH0645 #3421 or equivalent): $14.73 at
     Walmart in this search; Adafruit's own direct-list price is
     typically lower (historically ~$6–8) — use a range, reseller
     markup varies a lot for this part.
   - Kailh Choc V1 switches: no clean per-unit bulk price surfaced;
     community pricing knowledge puts these around $0.60–0.90/switch in
     small quantities.
   - MBK blank keycaps: €0.85/cap individually (42Keebs) down to about
     €0.69/cap in 10-packs (Keycapsss) — roughly $0.75–0.95/cap in USD.
   - C&K PCM12SMTR (if bought now, before obsolescence bites): $0.96 at
     DigiKey, $0.66–1.18 across other distributors.

## Bottom line

**Neither vendor gives a confident "yes, fully zero-solder" answer for
this BOM** the way v1's research suggested — the two modules are the
open question, and it genuinely depends on getting a real quote (likely
from PCBWay, given their consigned-parts process) rather than something
resolvable from search snippets. What *is* solid: the 5 keyswitches, the
passives, and the LED are all routine vendor-assemblable work at either
shop, and — the more important practical point — **hand-soldering the
two modules yourself is not the hard problem it used to be.** In the v1
BOM, "solder it yourself" meant reflow/hot-air for an LGA mic chip with
no accessible leads. In v2.1, both modules are big, friendly through-hole
header pins (14 + 6 = 20 joints, no fine pitch, no reflow) — genuinely
one of the easier parts of this build. That changes the cost-options
framing in `hardware/assembly_options.html`: full DIY is now realistic
for far more people than it was under the old BOM, and the "pay a vendor"
case rests on convenience/time, not on a skill/tooling barrier the way it
did before.

## Before committing to an order

Get a real PCBWay quote for the consigned/combo path (with the two
modules called out explicitly) before assuming either "zero solder" or
"vendor won't touch it" — this is the one thing search snippets
genuinely can't settle. Resolve the SW6 obsolescence (issue #16) before
finalizing any BOM for ordering. Per `docs/HANDOFF.md`'s standing rule:
no fab/parts order without Geoff's go-ahead.

---

## Appendix: v1 research (superseded, kept for the record)

<details>
<summary>Original 2026-07-02 findings, built against the bare-SMD-mic /
flush-mount XIAO / addressable-LED-that-was-later-dropped-then-restored
BOM. Click to expand.</summary>

Every part in the v1 BOM already had a JLCPCB assembly-library listing,
including the XIAO RP2040 module itself:

| Part | JLCPCB part # | Status |
|---|---|---|
| Seeed XIAO RP2040 module (bare/castellated) | C9900176459 | "New Arrivals" category; listing notes it needs an assembly fixture |
| Kailh Choc 1350 keyswitch | C9900088831 | "New Arrivals" category |
| C&K PCM12SMTR slide switch | C221841 | established catalog listing |
| Knowles SPH0645LM4H-B mic (bare chip) | C2686054 | established catalog listing |
| WS2812B LED | C2761795 (Worldsemi WS2812B_BT) | established catalog listing |

That listing was almost certainly for the *bare/castellated* XIAO SKU
meant for reflow — which turned out not to be the SKU Geoff actually
ordered, so this specific conclusion didn't carry forward. JLCPCB Economic
vs. Standard PCBA tier rules, THT wave-soldering costs, and MOQ figures
from that round are still accurate and repeated in the current findings
above where still applicable.

</details>
