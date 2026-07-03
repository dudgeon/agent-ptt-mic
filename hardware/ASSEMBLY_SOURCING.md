# Assembly sourcing — JLCPCB vs PCBWay (zero-solder feasibility)

**Current as of:** 2026-07-02, v2.1 BOM (pre-soldered/header XIAO, mic
breakout module, addressable RGB LED — see `hardware/BOM.md`). Supersedes
the v1 research kept as an appendix at the bottom of this file.

**Two research rounds went into this doc:** an initial search-snippet
round (below, "search-snippet round" heading) built entirely from
`WebSearch` because direct `WebFetch` of jlcpcb.com/pcbway.com returned
HTTP 403 every time — and a follow-up round on 2026-07-02 **with real
browser access** that re-verified the key open questions against live
vendor tools and documentation. The live-verification findings are the
most current and most trustworthy numbers in this file; the
search-snippet section is kept for its still-useful qualitative analysis
but its specific price figures are superseded where the live round found
different numbers.

## Live-verification round (2026-07-02, real browser access)

**Method:** live JLCPCB and PCBWay instant-quote tools, JLCPCB's own
Help Center policy pages, and PCBWay's Assembly quote calculator —
actual tool output, not search snippets. Board dimensions used: 44×104mm,
2-layer, qty 5, matching `hardware/design_params.py` `PCB_W`/`PCB_L`.
(At the time of this first pass the board was placed+netlisted but not
yet routed — issue #13 — so this was a dimension/qty/layer-count quote,
not a full Gerber-based DFM quote. **Update:** the board is now routed
and the real Gerbers have since been uploaded directly — see "Round 4"
below — and returned the identical price, confirming this estimate held.)

### Bare PCB fab: JLCPCB is dramatically cheaper than PCBWay for this board

| Vendor | Bare PCB cost (5 pcs) | Shipping (DHL, 2–4 days) | Total | Source |
|---|---|---|---|---|
| **JLCPCB** | **$2.00–$6.10** (varied between two identical-input quote runs — see note) | $28.72 | ~$31–35 | Live instant quote, [cart.jlcpcb.com/quote](https://cart.jlcpcb.com/quote), 2026-07-02 |
| **PCBWay** | $19.48 | $25.71 | $45.19 | Live instant quote, [pcbway.com/QuickOrderOnline.aspx](https://www.pcbway.com/QuickOrderOnline.aspx), 2026-07-02 |

This **corrects the prior estimate** of "$8–20/5-boards" downward for
JLCPCB — the 104mm side does not push this board out of JLCPCB's cheap
prototype tier the way the search-snippet round assumed. PCBWay is a
real, live-confirmed ~2–9x more expensive than JLCPCB for bare fab at
this specific size/qty, not a rough guess. (JLCPCB's own quote UI showed
$2.00 on the first pass and $6.10 after toggling build-time/other
options — the $4.00 delta was an "Engineering fee" that appeared on the
second calculation; re-verify at order time, but either figure is far
below the old estimate.)

### PCBA / consigned parts: JLCPCB officially supports it (with real, and real-ly not cheap, fees) — corrects the prior "JLCPCB likely declines" assumption

The prior round assumed JLCPCB's standard flow declines customer-supplied
parts. **That's wrong.** JLCPCB's own Help Center documents an overseas
consignment process (["How to consign parts to
JLCPCB"](https://jlcpcb.com/help/article/how-to-consign-parts-to-jlcpcb),
["Consignment Part Terms &
Conditions"](https://jlcpcb.com/help/article/consignment-part-terms-conditions),
both fetched live 2026-07-02) — but it comes with real, documented fees
that change the economics for a small prototype run:

- **Overseas consignment service fee: $70 per 50 part numbers + $15
  handling = $85 flat for 1–50 part numbers.** This is a **fixed fee per
  order, not per unit** — consigning just the XIAO module and the mic
  breakout (2 part numbers) costs the same $85 as consigning 50 different
  part numbers. For a 5-board prototype run this fee alone roughly
  doubles the project's total cost; it amortizes away only at much higher
  unit volumes.
- **Loose/separate-component fee:** $0.142/piece, since header-mounted
  modules aren't tape-and-reel and can't go straight onto the P&P line.
- **Manual handling fee:** $0.017/pin for parts with ≤5 pins, capped at
  $0.078/component for parts with more pins — both the XIAO (14 pins)
  and the mic breakout (6 pins) hit the $0.078 cap.
- **Recommended baking fee for moisture-sensitive modules:** $8/48 hours.
- Freight to ship the modules to JLCPCB's China warehouse, customs/duties
  on the way there, and (if picking up unused consigned stock afterward)
  return freight/customs are all **the customer's responsibility**, not
  included in any of the above.
- Each consigned part number needs "additional quantity... for attrition
  or minimum assembly requirement" — JLCPCB doesn't guarantee the full
  order builds without spare units.

**Net effect on Option D (`hardware/assembly_options.html`):** genuine
zero-solder via JLCPCB consignment is real and documented, but for a
5-unit prototype run the ~$85 flat service fee plus per-component
handling is a **new, previously-unknown fixed cost** that was not
priced into the old $260–470 estimate. This makes Option D *less*
attractive at prototype quantities than previously assumed, not more —
see the updated Option D figure in `assembly_options.html`.

### PCBA: PCBWay Combo/Consigned — real calculator estimate obtained

PCBWay's live SMT Assembly quote tool ([pcbway.com/quotesmt.aspx](https://www.pcbway.com/quotesmt.aspx))
confirms the "Combo" (customer supplies some parts) and "Kitted or
Consigned" (customer supplies all parts) options exist as first-class,
selectable order types — matching the prior round's finding. Filling in
representative BOM stats for this board (9 unique part numbers, 5 SMD
parts, 8 THT parts) at qty 5 in **both** modes returned the same
estimate:

- **Assembly service cost: $88.00 for 5 boards** ($17.60/board), before
  PCB fab cost and before the value of the parts themselves.
- Shipping quoted separately at $27.27 (a promotional discount canceled
  it out to $0 in this specific quote run — don't rely on that holding).

**Caveat:** this is PCBWay's generic calculator estimate from
part-count inputs, not a firm quote — it does not yet reflect PCBWay's
engineering review of the two irregular, tall, header-standoff-mounted
modules specifically. A firm number requires uploading real Gerbers + a
BOM/CPL with the actual XIAO and mic breakout parts called out, which
needs the board routed first (issue #13). Treat $88 as the current
best-available real number for Option C/D's assembly-service line, not
a guarantee PCBWay will place the modules without an extra manual-
placement surcharge once they see the actual parts.

### Round 3 (2026-07-02, later same day): board now routed, quotes re-run against the real BOM — same numbers hold, one new hard limit found

The carrier board is now actually routed and DRC-clean (`hardware/pcb/README.md`),
with a real Gerber zip at `hardware/pcb/fab/companion_carrier_v0_gerbers.zip`.
**Attempted to upload it directly to both JLCPCB and PCBWay for a true
DFM-reviewed quote — blocked, not by either vendor, but by this browser
session's file-sharing restrictions** (the extension will only upload
files from folders explicitly shared with the session; the repo's
`hardware/pcb/fab/` isn't one of them). So this round re-runs the same
manual-entry method as Round 1/2, with two upgrades: the bare-fab
dimensions are now for the actual final board (unchanged: 44×104mm,
2-layer), and the assembly part-counts are the real ones read off the
routed board's BOM instead of a generic guess.

- **JLCPCB bare fab: re-confirmed, unchanged.** $2.00 (with the site's
  running "Special Offer") rising to $6.10 once an "Engineering fee"
  line appears on recalculation — same behavior as Round 1. Shipping
  $28.72 DHL. Total ~$31–35 for 5 boards.
- **PCBWay bare fab: re-confirmed, unchanged.** $19.48 + $25.71 shipping
  = $45.19.
- **JLCPCB PCBA has no manual-entry path — confirmed by directly toggling
  it on the live quote page.** Flipping "PCB Assembly" on with no Gerber
  attached returns: *"Please upload Gerber files before proceeding to PCB
  Assembly."* This is a hard, categorical requirement, not a preference —
  unlike PCBWay, there is no dimension/part-count estimate available for
  JLCPCB's assembly service without a real file upload. Anyone wanting a
  JLCPCB PCBA number needs to upload the real zip themselves (or hand it
  to a session with file-sharing permission).
- **PCBWay Combo and Kitted/Consigned re-run with the board's real part
  counts** (8 unique part numbers, 1 SMD part [D1], 12 THT part instances
  [5 switches + SW6 + MK1 + U1 + C1/C2/C3 + R1] — not the earlier generic
  9/5/8 guess): **both modes returned the identical $88.00 for 5 boards**
  as Round 2's generic estimate. That the real BOM composition reproduces
  the same number is a good sign the $88 figure is stable, not an
  artifact of made-up inputs — though the caveat from Round 2 still
  applies (calculator estimate, not an engineering-reviewed firm quote
  for the two irregular modules specifically).

**Bottom line on getting a truly firm number:** the one thing that
still requires a human is uploading `companion_carrier_v0_gerbers.zip`
directly at cart.jlcpcb.com/quote or pcbway.com/QuickOrderOnline.aspx —
takes under a minute once the file's in front of you, and is the only
way to get a real DFM-reviewed quote (copper density, exact hole count,
solder-mask checks) rather than a dimension-based estimate. The
dimension-based numbers above have now been independently reproduced
three times and are a reliable stand-in until then.

### Round 4 (2026-07-02, same day): Geoff uploaded the real Gerbers — DFM-reviewed quotes confirmed on both vendors

Geoff placed `companion_carrier_v0_gerbers.zip` directly into both
vendors' quote tools (the file-sharing block from Round 3 is a browser-
automation limitation, not something a human hits). Both parsed it
cleanly with **no DFM errors or warnings**, just each vendor's standard
"auto-preview may not be pixel-perfect" disclaimer:

| Vendor | Detected board | PCB cost (5 pcs) | Shipping | Total | Source |
|---|---|---|---|---|---|
| **JLCPCB** | "2 layer board of 104×44mm (4.09×1.73 inches)" — exact match | $6.10 ($4.00 engineering fee + $2.10 board) | $28.72 DHL Express | **$34.82** | Live upload, [cart.jlcpcb.com/quote](https://cart.jlcpcb.com/quote), 2026-07-02 |
| **PCBWay** | "2 layers board of 44×104mm (1.73×4.09 inches)" — exact match | $19.48 | $25.71 DHL | **$45.19** | Live upload, [pcbway.com/QuickOrderOnline.aspx](https://www.pcbway.com/QuickOrderOnline.aspx), 2026-07-02 |

**These numbers are identical to the dimension-based estimates from
Rounds 1–3** — real Gerber upload changed nothing about the bare-fab
price for this board, which confirms the earlier estimates weren't
missing anything material (no unusual copper density, hole count, or
routing complexity that would have moved the price). Both vendors
showed the actual routed board preview (front + back copper visible),
confirming the file parsed correctly end to end.

**Assembly quoting hit the same wall from both sides:** JLCPCB requires
an account login before it will show a real BOM-based PCBA number (the
"PCB Assembly" toggle works once a Gerber is attached, but clicking
"Next" redirects to a login page). PCBWay's manual-entry assembly
estimate doesn't need login (still $88/5 boards, matching Rounds 2–3),
but actually adding the assembly order to cart — the step that would
let a real BOM/CPL get reviewed — also redirects to account login/sign-up.
**Neither of us created an account or logged in** — that's a real
account-creation/login action, out of scope for this pass. Getting a
firm PCBA number from either vendor now requires Geoff (or whoever owns
the order) to sign in themselves and carry the already-uploaded Gerber
into the assembly flow.

### What's still open after this round

- **Firm PCBA numbers from either vendor** — both require account
  login to get past the generic estimate stage; bare-fab numbers are
  now fully confirmed (Round 4), assembly numbers are not.
- **PCBWay's exact stance on placing the two specific irregular modules**
  (vs. a generic same-part-count board) is still unconfirmed — the $88
  figure is a calculator estimate, not an engineering-reviewed quote,
  and getting a real one needs the login step above.
- JLCPCB consignment's real-world friction (shipping modules to China,
  customs, lead time added) wasn't feasible to fully quantify without
  placing a real trial order — the fee schedule above is real and
  documented, but total elapsed time for a consignment order is still an
  estimate.

## Search-snippet round (superseded numbers below, kept for qualitative analysis)

**Method note, this round:** direct `WebFetch` of jlcpcb.com and
pcbway.com pages returns HTTP 403 (bot-blocked) every time, including
inside the automated deep-research workflow (21/21 sources failed there
on the first pass). This round is built from ~14 targeted `WebSearch`
queries against search-engine-indexed snippets — including community/
forum sources (EEVblog, Deskthority, Hackaday.io) alongside vendor pages
— triangulated across independent queries per claim. **Its specific
price figures for bare PCB fab and the JLCPCB consignment stance are
superseded by the live-verification round above** — the qualitative
analysis below (module-placement uncertainty, THT-soldering-is-easy
conclusion, etc.) still holds.

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
   though an exact figure needs the live quote tool. **Superseded —
   see the live-verification round above: JLCPCB's real live quote for
   this exact size/qty came back at $2.00–$6.10, not $8–20.** PCBA setup+stencil
   minimums cluster around $30–70 for a double-sided board at JLCPCB
   (one referenced July-2025 example: $33.66 minimum for single-sided
   Economic PCBA setup+stencil alone, before parts/labor). PCBWay's
   often-cited "$5 for 5-10 boards" figure is PCB fab only, not PCBA —
   don't conflate the two when reading vendor marketing pages.
6. **Whole-device, one vendor:** unchanged from v1 — JLCPCB+JLC3DP have a
   documented combined-order flow; PCBWay offers the same service breadth
   but combined ordering leans on contacting their sales team.
7. **Updated small-parts pricing (informs the cost artifact):** **all
   four figures below superseded by live prices confirmed 2026-07-02 —
   see `hardware/BOM.md`'s Electronics table for citations.** XIAO
   pre-soldered is **$4.90 direct from Seeed** (not $24), mic breakout is
   **$6.95 direct from Adafruit** (matching the low end of the old
   range, not the $14.73 reseller figure), Kailh Choc switches are
   **≈$0.90–1.05/switch** and MBK caps **≈$0.90–1.05/cap** (both from
   splitkb.com, matching the old estimates closely). Original
   search-snippet figures kept below for the record:
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

**Update from the 2026-07-02 live-verification round:** the "genuinely
depends on getting a real quote" conclusion above held up — but the real
quote changed the shape of the answer. JLCPCB *does* support consigning
the two modules (contrary to the prior assumption it would decline), but
the real, documented $85 flat overseas-consignment fee (plus per-part
handling) makes that path **less** attractive at 5-unit prototype
quantities than assumed, not more. PCBWay's Combo/Consigned calculator
returned a real $88 assembly-service estimate for 5 boards, which is
useful but still not an engineering-reviewed commitment to place the
specific irregular modules. Bare PCB fab is now confirmed cheap at
JLCPCB ($2–6 for 5 boards) and confirmed markedly pricier at PCBWay
($19.48) for this exact board size — a genuine, not estimated, reason to
default to JLCPCB for bare fab regardless of which vendor (if any) ends
up doing assembly.

## Before committing to an order

Get a **firm** PCBWay quote for the consigned/combo path with real
Gerbers + BOM/CPL and the two modules called out explicitly (the $88
figure above is a calculator estimate from part counts, not an
engineering-reviewed quote) — this needs the board routed first (issue
#13). Resolve the SW6 replacement pick (issue #16 — survey done, pick
still needs Geoff's sign-off, see `hardware/BOM.md`) before finalizing
any BOM for ordering. Per `docs/HANDOFF.md`'s standing rule: no fab/parts
order without Geoff's go-ahead.

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
