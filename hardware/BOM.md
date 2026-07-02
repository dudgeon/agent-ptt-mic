# Bill of Materials — Carrier PCB Track (v2.1)

> **Status: PROVISIONAL, not final.** Most of this table was originally
> picked by an AI design session with no live browser access to
> distributor stock/pricing pages (see `hardware/ASSEMBLY_SOURCING.md`'s
> method note and `docs/HANDOFF.md`). A follow-up session on 2026-07-02
> **with real browser access** re-verified SW6 (deep component survey,
> below), XIAO/mic breakout live pricing, and mic breakout physical
> dimensions against primary sources (Digi-Key, Mouser, LCSC, Seeed,
> Adafruit) — see each row's `Source` column and the SW6 callout for live
> citations. Everything else in this table (Kailh Choc, MBK caps, LED,
> passives) has **not** yet had the same live-source pass and should
> still be treated as a working draft, not a locked parts list, until it
> has.

Provisional part selections for the custom carrier PCB + handheld
enclosure track (`docs/PHYSICAL_DESIGN_SPEC.md`). The breadboard track's
BOM in `docs/SPEC.md` §7 is separate and unchanged.

**v2 revision (2026-07-02):** the XIAO Geoff actually ordered is the
**pre-soldered/header** SKU (`docs/SPEC.md` §4), not the bare-castellated
one v1 assumed — it mounts via its own presoldered pin headers, not a
flush reflow joint. At the same time, the mic switched from a bare SMD
chip to a breakout module (matching the original breadboard-track part).
Net effect: the XIAO, mic, switches, and passives are all through-hole/
header-mount — hand-solderable with a plain iron, no reflow needed for
any of them — at the cost of a thicker enclosure (~22.6mm vs. ~14.3mm in
v1), since the header-mounted module needs real standoff clearance
instead of sitting flush.

**v2.1 revision (same day):** Geoff asked for the status LED to be RGB.
A genuine discrete RGB LED needs 3 independent GPIOs; the locked pin map
(`docs/SPEC.md` §8) only has 2 spares. Rather than touch the pin map, D1
reverts to an **addressable** RGB LED (WS2812B/SK6812-style) — the only
way to get full RGB from the one GPIO the budget actually has spare.
Firmware only needs to emit solid colors (no animation requirement), but
still has to speak the WS2812 protocol to do that. This is the one
deliberately-reintroduced SMD part on the board — still hand-solderable
(large gull-wing pads, not a reflow-only part like the old mic chip was).

See `hardware/assembly_options.html` for the cost/effort comparison this
enables (**pending a rebuild reflecting v2.1** — see
`docs/PHYSICAL_DESIGN_SPEC.md` §7 for the full rationale on both
revisions).

Per project convention: **verify availability and datasheet revisions before
placing any order** — and per `docs/HANDOFF.md`, don't order fab or parts
without checking with Geoff first.

## Electronics

| Ref | Qty | Part | Package / mount | Why this part | Source |
|---|---|---|---|---|---|
| U1 | 1 | Seeed Studio XIAO RP2040 — **pre-soldered** | Header pins, mounted on carrier BACK via its own presoldered pins pushed through + soldered | [LOCKED] board choice; module carries USB-C, RP2040, flash, NeoPixel | [Seeed, pre-soldered](https://www.seeedstudio.com/Seeed-Studio-XIAO-RP2040-Pre-Soldered-p-6333.html) — **$4.90/unit confirmed live 2026-07-02** (US direct-from-Seeed, in stock; $4.40 at 10+), well below the earlier $9–24 search-snippet estimate |
| SW1–SW5 | 5 | Kailh Choc V1 (PG1350) — Brown/tactile suggested | Through-hole switch pins + locating posts | Low-profile mechanical keyswitch: real switch feel in a handheld-thickness shell (11 mm stack vs ~18.5 mm for full MX) | Kailh via distributors (Chosfox, splitkb, MoErgo, AliExpress) — [splitkb.com](https://splitkb.com/collections/switches) confirmed live 2026-07-02: €0.99/switch single, €0.82 excl. tax in packs (≈$0.90–1.05 USD) |
| — | 5 | MBK Choc-profile 1u keycaps, blank | Friction-fit on Choc stem | Blank per the minimalist/UV-print decision | Same suppliers as switches — [splitkb.com](https://splitkb.com/collections/keycaps) confirmed live 2026-07-02: €0.99/cap single, €0.82 excl. tax in packs (≈$0.90–1.05 USD), matching the earlier estimate closely |
| SW6 | 1 | ~~C&K PCM12SMTR~~ — **under review, see survey below** | Right-angle SMT, actuator past PCB edge | Latch control on the shell *side wall* per §2.3; distinct-by-feel from the keys | Deep component survey completed 2026-07-02 with live distributor data — see callout below. **C&K OS102011MA1QN1 is the [PROPOSED] leading replacement**, pending Geoff's sign-off and a body-height clearance check |
| MK1 | 1 | I2S MEMS mic **breakout module** (e.g. Adafruit SPH0645, PID 3421) | 6-pin THT header, front side, own onboard acoustic port | Matches the original breadboard-track part (SPEC §7 OQ2) instead of a bare reflow-only chip — hand-solderable header pins | [Adafruit #3421](https://www.adafruit.com/product/3421) — **$6.95/unit confirmed live 2026-07-02** (direct from Adafruit, in stock; $6.26 at 10+), matching the earlier estimate. Official dimensions **16.7 × 12.7 × 1.8mm** (resolves the `MIC_BRK_L`/`MIC_BRK_W` VERIFY tags in `hardware/design_params.py`) |
| D1 | 1 | WS2812B (5050) or SK6812 addressable RGB LED | SMD, front side, top edge | v2.1: full RGB "for future status options," reintroduced as addressable because the pin budget only has 1 spare GPIO left (see revision note above) — driven with solid colors only, no animation requirement | Commodity |
| C1 | 1 | 100 nF THT ceramic disc | THT, 5mm lead spacing | Mic VDD decoupling | Commodity |
| C2 | 1 | 100 nF THT ceramic disc | THT, 5mm lead spacing | LED decoupling | Commodity |
| C3 | 1 | 10 µF THT electrolytic/ceramic | THT, 5mm lead spacing | Bulk for LED + mic rail | Commodity |
| R1 | 1 | 300–500 Ω 1/4W axial resistor | THT, formed leads | LED data-line series resistor (signal integrity, not current-limiting — WS2812 draws its own current) | Commodity |

> ## ⚠ SW6 (latch switch) — component survey complete (2026-07-02, live browser pass), pick still [PROPOSED]
>
> **Survey done with real browser access** (DigiKey, Mouser, LCSC live
> parametric search + product pages, not search snippets). C&K PCM12SMTR
> is still real and still orderable at some distributors, but this pass
> confirms the obsolescence risk *and* surveys genuine alternatives
> outside the SMT-slide-switch box, per the filter criteria below.
> **None of the candidates below are ordered or locked — this is a
> recommendation for Geoff to confirm, matching every other [PROPOSED]
> item in this file.**
>
> **The actual requirement** (unchanged from the prior write-up, still the
> filter to design against): `docs/SPEC.md` §2 Message 1 only asked for "a
> switch that sets the microphone to always stream" — no mechanical type,
> mounting, or manufacturer specified. `docs/SPEC.md` §3 Locked Decision 6
> implies a **physical, visibly-stateful** control (weakens the case for a
> momentary-button-with-firmware-latch, even though that would satisfy the
> letter of the requirement). `docs/PHYSICAL_DESIGN_SPEC.md` §2.2's "must
> feel distinct from a Kailh Choc key" is this project's own inference,
> not a Geoff requirement — still reasonable, but re-confirm rather than
> treat as locked.
>
> **Candidates surveyed, with live stock/pricing (checked 2026-07-02):**
>
> | Candidate | Category | Mounting | Price @1 (qty break) | Stock (live) | Distributors confirmed | Fit notes |
> |---|---|---|---|---|---|---|
> | **C&K OS102011MA1QN1** — *leading candidate* | Slide, SPDT, on-on | **Through-hole, right-angle** (same edge-mount concept as PCM12 — actuator exits past the PCB edge) | $0.71 ([DigiKey](https://www.digikey.com/en/products/detail/c-k/OS102011MA1QN1/1981430)), $0.70 ([Mouser](https://www.mouser.com/c/?q=OS102011MA1QN1)), $0.66 ([LCSC C226259](https://www.lcsc.com/search?q=OS102011MA1QN1)) | DigiKey 91,153 · Mouser 16,403 · LCSC 2,711 | **3** (DigiKey, Mouser, LCSC) | Active, 10,000-cycle mechanical life, 4.00mm actuator length, 2.00mm travel. LCSC's facet data lists this THT body as ~8.6×4.7mm footprint and ~8.4mm tall above the PCB — **notably taller than PCM12's 3.4mm SMT body**, likely taller than the current `CHOC_H_ABOVE_PCB` (5.0mm) front-side clearance envelope. **VERIFY against the datasheet mechanical drawing before finalizing** — may need a local clearance bump, not a full enclosure redesign, but don't assume it fits FRONT_GAP as-is. |
> | **E-Switch EG1218** | Slide, SPDT, on-on | Through-hole, **vertical** (slider parallel to PCB face — like the mic/LED mounting concept, not the side-wall pass-through) | $0.72 ([DigiKey](https://www.digikey.com/en/products/detail/e-switch/EG1218/101726)), $0.71 ([Mouser](https://www.mouser.com/c/?q=EG1218)), $1.26 ([LCSC C273394](https://www.lcsc.com/search?q=EG1218)) | DigiKey 33,119 · Mouser 13,254 · LCSC 156 | **3** (DigiKey, Mouser, LCSC) | Active. Cheapest at scale, widest stock, but the vertical-slider orientation means SW6 would move from "knob pokes out the side wall" to "slider pokes up through a top-face slot" — a real layout change, not a drop-in swap, so it needs a `PHYSICAL_DESIGN_SPEC.md` §2.3 re-think if picked over OS102011. |
> | **CIT Relay & Switch ANT11SF1CQE** | Toggle, SPDT, on-on (bat handle) | Through-hole, vertical, unthreaded bushing | $2.36 ([DigiKey](https://www.digikey.com/en/products/detail/cit-relay-and-switch/ANT11SF1CQE/12503396)) | DigiKey 7,191 (14-week mfr lead time on restock, but current DigiKey stock covers small qty) | **1 so far** (not found on Mouser or LCSC in this pass — re-check before relying on it) | Active, 50,000-cycle life, 10.67mm actuator. A toggle is the most *visibly* stateful option of anything surveyed (flipped-up vs. flipped-down is unmistakable even at a glance, more so than a slide) — directly reinforces the §3 Locked Decision 6 spirit. Needs a round panel cutout instead of the current rectangular slide slot — bigger enclosure change than either slide option. Single-distributor risk is real; would want a second source confirmed before committing. |
> | NKK MN12TXG13-DA | Rocker, SPDT, on-on | Through-hole | $10.08 ([DigiKey](https://www.digikey.com/en/products/filter/rocker-switches/195)) | 223 | 1 | Active but ~14x the cost of the slide options and bulkier (rectangular rocker cap, typically wants a panel cutout). Viable if Geoff wants a rocker specifically; not cost-competitive otherwise. |
> | Knitter-Switch SMR 1-30 | Rotary, 2-position, screwdriver-slot actuator | PCB mount | $2.07 | 1,886 | 1 | Compact and cheap, but the screwdriver-slot actuator needs a tool to change state — fails the "visibly/tactilely stateful by hand" spirit of §3 Locked Decision 6 unless paired with a knob-actuator rotary (those ran $10–18 in this survey, e.g. C&K A11405RNZQ). Not recommended given the cost/complexity vs. the slide/toggle options above. |
> | Momentary + firmware latch (reuse a Kailh Choc key, no new part) | — | — | $0 incremental (already in BOM) | — | — | Cheapest and simplest option architecturally, but state lives only in firmware — no physical position to check by eye or touch, weakening the §3 Locked Decision 6 guarantee. Listed for completeness per the filter criteria; **not recommended** unless Geoff explicitly prefers it over a mechanical switch. |
>
> **Recommendation (flagged [PROPOSED], not decided):** **C&K
> OS102011MA1QN1** as primary pick — it's the closest geometric match to
> the current side-wall-slot mounting concept (right-angle THT, actuator
> past the board edge, same mental model as PCM12 just through-hole
> instead of SMT), confirmed active and in stock at 3 independent
> distributors, and cheap ($0.66–0.71). The one open item before treating
> this as final: **confirm its through-PCB body height against
> `CHOC_H_ABOVE_PCB`/`FRONT_GAP`** — the LCSC facet data suggests it may
> be taller than the SMT part it replaces. E-Switch EG1218 is the
> fallback if that clearance check fails, at the cost of moving SW6 to a
> top-face slot. CIT ANT11SF1CQE (toggle) is worth a look if Geoff wants
> the most unambiguous physical-state affordance and is fine with a
> bigger enclosure change and a currently-single-sourced part.
>
> Tracked as [GitHub issue #16](https://github.com/dudgeon/agent-ptt-mic/issues/16).
> Footprint/pin spacing in `hardware/pcb/generate_pcb.py` (`slide_pcm12()`)
> and the `SLIDE_*` constants in `hardware/design_params.py` are
> **unchanged in this pass** — deliberately left alone until Geoff signs
> off on one of the above, per the issue's explicit scope boundary
> ("actually picking a replacement... is the next step after the
> survey, not this one").

Optional (decided against for v2, easy to add later): Kailh Choc hot-swap
sockets (CPG135001S30) — v2 solders switches directly for simplicity and
lower back-side height.

**Superseded from v1** (kept here for history, not for ordering): Knowles
SPH0645LM4H-B bare SMD chip, 0603 SMD passives.
**Superseded from v2** (briefly, same day): plain 3mm THT LED — reverted
to addressable in v2.1 per the pin-budget constraint above.

## Enclosure hardware

| Qty | Part | Purpose |
|---|---|---|
| 4 | M2 × 16 mm self-tapping screws | Back lid → spacer boss → PCB → front-shell boss (stack now ≈ 2 + 11.5 + 1.6 mm + ~4 mm thread engagement, up from the v1 flush-mount stack — the header-mounted module pushed BACK_GAP out to 11.5mm) |
| 1 | FDM print, 2 parts (front + back shell) | `hardware/enclosure/` outputs |

## Electrical connections (carrier netlist summary)

Pin assignments preserve `docs/SPEC.md` §8 exactly; the only addition is the
status LED on previously-spare D10.

| XIAO pad | GPIO | Net | Connects to |
|---|---|---|---|
| D0 | GPIO26 | `PTT` | SW5 (push-to-talk key) → GND |
| D1 | GPIO27 | `LATCH` | SW6 (slide) common → GND |
| D2 | GPIO28 | `KEY_APPROVE` | SW1 → GND |
| D3 | GPIO29 | `I2S_SD` | MK1 DATA |
| D4 | GPIO6 | `I2S_BCLK` | MK1 BCLK |
| D5 | GPIO7 | `I2S_LRCLK` | MK1 WS/LRCLK |
| D6 | GPIO0 | `KEY_REMEMBER` | SW2 → GND |
| D7 | GPIO1 | `KEY_REJECT` | SW3 → GND |
| D8 | GPIO2 | `KEY_MODE` | SW4 → GND |
| D9 | GPIO4 | spare | — |
| D10 | GPIO3 | `LED_DATA` | R1 → `LED_DIN` → D1 DIN |
| 3V3 | — | `3V3` | MK1 VDD, D1 VDD, C1–C3 |
| GND | — | `GND` | all switches, MK1 GND + SEL (left ch.), D1 GND |

Note on the LED (v2.1): D1 is addressable (WS2812B/SK6812-style), so
GPIO3 carries the WS2812 single-wire data protocol through R1 to DIN, not
a simple high/low current-limited drive. D1's DOUT is left unconnected
(not chained to a second LED). WS2812B is a 5V part that generally runs
fine at 3.3V with a 3.3V data signal; swap to SK6812 (native 3.3V) if
brightness/reliability disappoints. All button/switch inputs use the
RP2040 internal pull-ups, active-low, no external resistors (SPEC §8
convention).
