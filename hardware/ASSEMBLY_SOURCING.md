# Assembly sourcing — JLCPCB vs PCBWay (zero-solder feasibility)

> **⚠ Superseded by the 2026-07-02 mounting revision — re-verify before
> trusting this.** This research and `hardware/assembly_options.html` were
> both done against the *original* BOM: a bare-castellated XIAO meant for
> flush reflow, a bare SMD mic chip, and an SMD WS2812B LED. The board has
> since changed to match the XIAO Geoff actually ordered (pre-soldered/
> header SKU) plus a mic breakout module and a plain THT LED — see
> `hardware/BOM.md` and `docs/PHYSICAL_DESIGN_SPEC.md` §7. The JLCPCB
> "XIAO RP2040" library listing below (C9900176459, needs an "assembly
> fixture") was almost certainly for the bare/castellated SKU meant for
> automated reflow placement — a header-pin module standing off the board
> on its own pins isn't a typical pick-and-place or wave-solder candidate.
> **Practical effect:** full zero-solder turnkey (assembly_options.html
> option D) is now doubtful specifically for the XIAO module — the
> switches, mic breakout, and LED/passives are still ordinary THT vendor
> work, but the module itself (14 big, easy pins) may be the one part
> worth self-soldering even in an otherwise-turnkey order. This needs a
> fresh vendor check, not a guess — flagged rather than silently
> reconciled.

**Researched:** 2026-07-02 (pre-revision). **Method note:** direct `WebFetch` of jlcpcb.com and
pcbway.com pages returned HTTP 403 (bot-blocked) for every attempt, including
inside the automated deep-research workflow (21/21 sources failed there).
Everything below comes from search-engine-indexed snippets, triangulated
across multiple independent queries per claim. Treat anything not phrased as
"confirmed" as needing a live quote-tool check, not settled fact.

## Headline finding

Every part in `hardware/BOM.md` already has a JLCPCB assembly-library listing,
including the XIAO RP2040 module itself:

| Part | JLCPCB part # | Status |
|---|---|---|
| Seeed XIAO RP2040 module | C9900176459 | "New Arrivals" category; **listing notes it needs an assembly fixture** |
| Kailh Choc 1350 keyswitch | C9900088831 | "New Arrivals" category |
| C&K PCM12SMTR slide switch | C221841 | established catalog listing |
| Knowles SPH0645LM4H-B mic | C2686054 | established catalog listing |
| WS2812B LED | C2761795 (Worldsemi WS2812B_BT) | established catalog listing |

If this holds on a live quote, JLCPCB could source 100% of the BOM from its
own stock — no consigned/customer-shipped parts needed at all.

PCBWay: SPH0645LM4H-B confirmed directly (dedicated component detail page).
WS2812B well-represented in their component/project catalog. Could **not**
confirm a PCBWay library listing for the Kailh Choc switch or the XIAO
module specifically — these would more likely need customer-supplied/
consigned parts there.

## Q&A summary

1. **Parts tiers.** JLCPCB: Economic PCBA (pre-loaded Basic-parts feeders, no
   per-part fee, capped at 30 pcs/design) vs. Standard PCBA (any library
   part, flat $1.50/part-line loading fee, no quantity cap). Sensors,
   fixture-needed parts, and anything smaller than 0201 are "Standard-only"
   — the mic and the XIAO module almost certainly force this board onto
   Standard PCBA. PCBWay: turnkey / consigned / combo sourcing modes;
   didn't find an equally precise tier breakdown.
2. **THT soldering.** JLCPCB explicitly assembles through-hole parts via
   wave/selective soldering, billed as an add-on (~$3.50 hand-soldering
   labor + ~$0.0135–0.0173/joint) — done by JLCPCB, not the customer.
   PCBWay offers THT assembly too; couldn't pin down an equally detailed
   cost breakdown.
3. **Mic/LED in-library:** confirmed at both vendors (see table above).
4. **Consigned XIAO module:** likely unnecessary at JLCPCB given its own
   listing exists. If that listing's stock/price doesn't check out,
   JLCPCB's consignment fallback exists but is pricey for a small run
   (loose-part handling fee; overseas consignment ~$70–155 in service +
   handling fees per the terms page). PCBWay more likely needs consignment
   for the module.
5. **MOQ/pricing:** JLCPCB PCBA minimum is 2 assembled boards (from a
   minimum-5 PCB fab order) on both Economic and Standard tiers — fits the
   2-10 unit target. PCBWay has no hard minimum but a $25 order floor.
   Neither gave a trustworthy dollar figure for this specific board from
   search snippets alone — needs a real quote upload.
6. **Whole-device, one vendor:** JLCPCB + JLC3DP have a documented
   "combine order" flow — PCBA and 3D-printed parts share one cart/
   checkout. PCBWay offers the same service breadth (CNC, 3D printing,
   sheet metal) but combined ordering pointed toward emailing their sales
   team rather than an integrated cart.
7. **Kailh Choc in automated PCBA:** has its own JLCPCB catalog part number
   (not just generic THT support), suggesting real placement experience
   with this exact part on their line.

## Bottom line

JLCPCB looks like the stronger fit for zero-customer-soldering and a
one-vendor whole-device order: every BOM part (including the module)
already has a library listing, THT is an explicit vendor-performed service,
and JLCPCB+JLC3DP combine into one checkout for PCB+enclosure. PCBWay can
very likely do the PCBA too, but the keyswitch specifically looks less
certain to be in their own stock.

## Before committing to an order

Upload `hardware/pcb/companion_carrier.kicad_pcb` + the BOM to JLCPCB's live
quote tool to confirm: real stock/price on the two "New Arrivals" listings,
whether the module's "assembly fixture" note adds cost/MOQ restrictions, and
actual per-unit PCBA pricing for this board. Search snippets can't verify
any of that — this doc is a starting point for that quote, not a
substitute for it. Per `docs/HANDOFF.md`'s standing rule: no fab/parts order
without Geoff's go-ahead.
