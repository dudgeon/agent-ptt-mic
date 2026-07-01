# Claude Code Companion Peripheral — Project Specification

**Status:** Pre-hardware-arrival, breadboard-planning phase
**Prepared for:** Handoff to a coding agent starting with no prior context
**Prepared:** July 1, 2026 (conversation-derived; verify time-sensitive facts before acting)

---

## 0. How to use this document

This is the single source of truth for a hardware/firmware project that began as a conversation and has **no other record**. Sections are labeled by confidence:

- **[LOCKED]** — explicitly decided by the project owner (Geoff). Do not revisit without asking.
- **[PROPOSED]** — recommended by the prior design conversation, not yet explicitly re-confirmed in the owner's own words. Treat as the working default, but flag it back to Geoff at the first natural checkpoint rather than silently assuming it's final.
- **[OPEN]** — a real decision point that has not been made. Blocks or partially blocks specific milestones (noted).

If you are the coding agent picking this up: read Sections 3–5 first (verbatims, locked decisions, open questions) before touching anything else. Section 12 is the actual work plan.

---

## 1. Project summary

A single custom hardware peripheral that plugs into a computer over one USB-C cable and — **without installing any driver** — is recognized simultaneously as a USB keyboard (HID) and a USB microphone. It has physical controls for: activating/deactivating the microphone, latching the microphone to always-on, and sending the keystrokes Claude Code uses for its permission/approval prompts. The goal is a tactile, dedicated control surface for voice input and approval-flow control while running Claude Code, rather than doing both through the host keyboard.

---

## 2. Customer verbatims (Geoff, in original order)

These are exact quotes from the project owner, preserved verbatim because they are the ground truth for requirements. Anything in this spec that isn't traceable to one of these (or to an explicit follow-up decision) is Claude's inference and is labeled as such.

**Message 1 (initial ask):**
> "I have a new idea for a project: a single peripheral that plugs into my computer via usb c and is recognized, without drivers, as both a keyboard and a microphone.
>
> This device has a small number of buttons, all three are programmable:
> - one activates the microphone, streaming audio to the computer
> - one is a switch, that sets the microphone to always stream
> - the remaining buttons are used to send the keystroke(s) that Claude code uses to receive approvals for actions, plans, etc (we may need a few of these if the different approval states requires keyboard shortcuts — I want to cover all of the most common)
>
> What is the minimal hardware board that can achieve these things? I am open to a custom pcb (you would design it) or a programmable microcontroller.
>
> The no driver requirement is hard, as is the single usbc plug for power and data."

**Message 2:**
> "Please give me links to the parts and verify the exact live bindings for Claude code shortcuts"

**Message 3:**
> "I'm going to go with the Seeed Studio XIAO RP2040 (adafruit option not available)
>
> There are so few visible I/o contacts; how do we handle all of the button io? Are there breakout boards available? Would we make a custom pcb for breakout?"

**Message 4:**
> "We will go with preordered and breadboard for now, and make a custom pcb once the design is locked.
>
> What's next?"

**Message 5 (this handoff request):**
> "Please give me a detailed write up of the project requirements including customer verbatims (mine) and locked decisions (eg the board I bought but has not arrived) and the work to be done. Spec is for handoff to coding agent to continue the project and will be a fresh start so it needs to be ultra detailed — if you miss details here they will be lost forever."

**Note on Message 1's button count:** Geoff wrote "all three are programmable" but then listed what reads as more than three physical items (one mic-activate button, one always-stream switch, and "the remaining button**s**" plural for keystrokes — implying more than one keystroke button). This spec interprets "three" as three *categories* of control (activate / latch / keystroke-send), not a literal cap of three physical buttons, and a follow-up design pass (Section 8) landed on 6 physical controls total. **This interpretation has not been explicitly re-confirmed by Geoff — flag it back to him.**

---

## 3. Locked decisions [LOCKED]

1. **Board: Seeed Studio XIAO RP2040.** Geoff has already ordered this board. **It has not yet arrived.** No further board-selection work is needed or wanted — do not revisit this choice.
   - Product family page: https://www.seeedstudio.com/XIAO-RP2040-v1-0-p-5026.html
   - Wiki/reference: https://wiki.seeedstudio.com/XIAO-RP2040/
   - The Adafruit QT Py RP2040 (functionally similar) was the original recommendation but was unavailable to purchase at decision time; the XIAO RP2040 was chosen as the in-stock equivalent.

2. **No-driver requirement is hard.** The device must enumerate using only classes natively supported by the OS out of the box: USB HID (keyboard) and USB Audio Class (microphone). No custom driver, kernel extension, or install step is acceptable on any target OS.

3. **Single USB-C connector for both power and data is hard.** No separate power jack, no battery in the current design, no second cable. Bus-powered only.

4. **Prototyping sequence:** breadboard the pre-ordered XIAO RP2040 first; **do not start custom PCB layout until the breadboard design is functionally locked** (Section 12, Milestone 7 gate).

5. **Composite USB device:** the single physical peripheral must present as *both* a keyboard and a microphone at the same time over the same port — not a switchable mode, not two cables, not a hub with two separate devices (a hub-based fallback was discussed as a hardware de-risking option in early exploration but is superseded now that the XIAO RP2040 module path was chosen — see Section 14).

6. **Privacy-preserving mic design pattern:** the USB Audio microphone interface should stay continuously enumerated at the USB level. Whether the host actually receives real audio or silence is gated in firmware by the physical push-to-talk / always-stream controls — not by dis/re-enumerating the USB interface. This was an explicit design goal from the original exploration (a hardware-enforced guarantee that nothing can be secretly listening unless a physical control is engaged) and should be preserved in implementation.

---

## 4. Board arrival — action items when it lands [OPEN, blocks Milestone 1]

Geoff ordered the board but it has not arrived as of this spec's writing. **Before starting firmware bring-up, confirm:**

- **Which SKU/variant actually shipped.** Seeed sells at least two relevant variants:
  - Headers included, unsoldered: https://www.seeedstudio.com/XIAO-RP2040-v1-0-p-5026.html
  - Pre-soldered (pins already attached, ready for breadboard): https://www.seeedstudio.com/Seeed-Studio-XIAO-RP2040-Pre-Soldered-p-6333.html
  - **This matters immediately**: a bare/header-included board needs the header strip soldered on before it can go into a breadboard at all. If the unsoldered variant arrived, soldering headers is the literal first physical step, before any firmware work.
- Visually confirm the board is the RP2040 variant (not a different XIAO family member — Seeed's XIAO line includes SAMD21, nRF52840, ESP32-S3, MG24, and others with different pinouts and capabilities; only the RP2040 variant matches everything in this spec).

---

## 5. Open decisions [OPEN — resolve before/during the listed milestone]

| # | Decision | Recommended default | Blocks | Owner |
|---|---|---|---|---|
| OQ1 | Firmware toolchain: **Pico SDK (C) + TinyUSB** vs. **Arduino + Adafruit TinyUSB core** | Pico SDK + TinyUSB — this is where the reference USB-Audio-Class mic examples live (`uac2_headset`, `audio_4_channel_mic`) and gives direct control over the composite USB descriptor. Arduino is a lighter option for HID-only experiments but is thinner on audio-class support. **CircuitPython is ruled out** — it has excellent HID support but does not expose a USB Audio Class device at all, so it cannot satisfy the microphone half of the requirement. | Milestone 1 (can't start without this) | Geoff / engineering |
| OQ2 | Microphone part — not yet purchased | SPH0645LM4H I2S MEMS mic, Adafruit #3421 (https://www.adafruit.com/product/3421). Alternative: ICS-43434, Adafruit #6049 (https://www.adafruit.com/product/6049) — note Adafruit's own listing states the ICS43434 has been discontinued and the SPH0645 is a drop-in replacement, so SPH0645 is the safer buy. Budget/no-link-verified alternative: INMP441 modules (widely available, same I2S interface). | Milestone 5 only (M1–M4 use a synthetic tone, no physical mic needed) | Geoff |
| OQ3 | Claude Code keystroke targeting strategy | See Section 10 for full detail. Two options: (a) hardcode the current default prompt keys (`1`/`Enter`, `2`, `Esc`, `Shift+Tab`) — simplest, but Claude Code ships weekly and default bindings have changed before; or (b) have the device target a **custom, explicit keybindings.json** config that Geoff installs once via Claude Code's own `/keybindings` command — more setup, but immune to upstream default-binding drift. **Not resolved; recommend (b) for durability but flag the extra one-time setup cost.** | Milestone 6 | Geoff / engineering |
| OQ4 | Behavior when push-to-talk *and* always-stream are both active simultaneously | Proposed: always-stream takes priority (mic stays live regardless of push-to-talk state). Not yet confirmed. | Milestone 6 | Engineering |
| OQ5 | What exactly fills the audio buffer when the mic is gated "off" — literal digital silence vs. low-level comfort noise | Proposed: literal silence (all-zero samples) unless testing reveals a host/app-side issue with dead air. | Milestone 5–6 | Engineering |
| OQ6 | Which operating systems must be validated for the "no drivers" requirement | Geoff's own machine is confirmed relevant (macOS, based on prior context). Whether Windows and/or Linux validation is required for this specific personal device is **not confirmed** — do not assume a broader deployment audience (e.g. Geoff's work context involves a large population of PMs, but nothing in this conversation ties this specific peripheral to that population). Ask before investing in multi-OS test rigs. | Milestone 4 | Geoff |
| OQ7 | Plan-mode approval (a multi-option menu, not a simple yes/no — see Section 10) currently has no dedicated button | Proposed: not needed for v1; the existing "Approve" button sending `Enter` will select whatever option is highlighted as default. Revisit if that proves insufficient in practice. | Not blocking; noted so it isn't lost | Geoff |

---

## 6. Non-goals (inferred, not explicitly confirmed — flag to Geoff)

To prevent scope creep during implementation, the following are assumed **out of scope** for this build unless Geoff says otherwise. None of these were explicitly ruled out or in — they are Claude's inference from "a single peripheral... single usbc plug":

- No wireless/Bluetooth connectivity.
- No on-device display or screen.
- No on-device storage or logging of audio/transcripts.
- No wake-word or on-device speech processing — the device is a dumb audio pipe; all intelligence is on the host.
- No support for pairing with multiple hosts simultaneously.
- No battery/portable power (explicitly ruled out by the "single USB-C for power and data" hard constraint).

---

## 7. Hardware bill of materials

### Locked / in hand (pending arrival)
| Part | Status | Link |
|---|---|---|
| Seeed Studio XIAO RP2040 | **[LOCKED]** Ordered, not arrived. Variant (pre-soldered vs. headers) unconfirmed — see Section 4. | https://www.seeedstudio.com/XIAO-RP2040-v1-0-p-5026.html |

### Needed, not yet purchased
| Part | Purpose | Recommended link |
|---|---|---|
| I2S MEMS microphone breakout | Audio input | SPH0645: https://www.adafruit.com/product/3421 |
| 4× tactile momentary switches | Approve / Approve+remember / Reject / Mode-toggle buttons, plus push-to-talk (5 total momentary, see pin map) | Commodity part, no SKU chosen |
| 1× slide or toggle switch | Always-stream latch | Commodity part, no SKU chosen |
| Breadboard + jumper wires | Prototyping | N/A |
| USB-C cable (data-capable) | Programming/power during dev | N/A |

### Deferred to future PCB phase — not needed now
See Section 14. Do not purchase these yet.

---

## 8. Pin assignment map [PROPOSED — not yet re-confirmed by Geoff after board choice]

The XIAO RP2040 exposes 11 usable GPIO on its edge pads, labeled D0–D10 by Seeed. This project needs 9, leaving 2 spare. Confirmed pin-to-GPIO mapping (source: TinyGo board definition, cross-referenced with Seeed's own pinout docs):

| XIAO pad | RP2040 GPIO | Assigned function |
|---|---|---|
| D0 | GPIO26 | Push-to-talk button (momentary) |
| D1 | GPIO27 | Always-stream switch (latching) |
| D2 | GPIO28 | "Approve" button → sends `Enter` |
| D3 | GPIO29 | I2S data in (mic SD/DOUT) |
| D4 | GPIO6 | I2S bit clock (BCLK) |
| D5 | GPIO7 | I2S word-select / LRCLK |
| D6 | GPIO0 | "Approve + remember" button → sends `2` |
| D7 | GPIO1 | "Reject" button → sends `Esc` |
| D8 | GPIO2 | "Mode toggle" button → sends `Shift+Tab` |
| D9 | GPIO4 | Spare |
| D10 | GPIO3 | Spare |

**Hard constraint driving this layout:** the RP2040 has no dedicated I2S hardware peripheral — I2S is implemented via the PIO (programmable I/O) subsystem, and the standard RP2040 I2S libraries (MicroPython's `machine.I2S`, pico-extras) require **BCLK and LRCLK to be on consecutive GPIO numbers**. That's why BCLK/LRCLK landed on GPIO6/GPIO7 specifically rather than more "logical" adjacent D-pad numbers.

**Microphone SEL pin:** tie to GND to select the left channel (the SPH0645/ICS-43434 mono mics use this pin to choose which I2S channel slot they occupy; GND = left, VDD = right).

**Button/switch wiring convention:** use the RP2040's internal pull-up resistors on every button/switch GPIO; wire the other side of each switch to GND. This means all controls are **active-low** (GPIO reads LOW when pressed/engaged) and need no external resistors.

**Onboard LED reference** (fixed silicon pins, not on the edge pads — free to use for status indication):
- WS2812/NeoPixel RGB LED: GPIO12 (power/enable: GPIO11)
- Discrete user LED: red = GPIO17, green = GPIO16, blue = GPIO25
- **Important quirk (from Seeed's own wiki):** on the XIAO RP2040, these programmable LEDs are **active-low** — the pin must be pulled low to light the LED, which is the reverse of typical Arduino LED convention. Account for this or you'll ship an "always on except when active" status light by accident.

**Known coincidental pin overlaps with RP2040 default peripheral assignments** (not a conflict today, since none of these hardware peripherals are used, but relevant if the design grows):
- D2/D3 are the RP2040's conventional I2C0 SDA/SCL pins.
- D4/D5 are the conventional I2C1 SDA/SCL pins (already consumed here by I2S clocks).
- D6/D7 are the conventional UART0 TX/RX pins.
- D8/D9/D10 are the conventional SPI0 SCK/SDI/SDO pins.
- **None of this blocks the current design** since no I2C, UART, or SPI hardware peripheral is used. Flagging only so a future feature addition (e.g., an SPI debug display, or an I2C GPIO expander like an MCP23017 for more buttons) doesn't collide with an already-assigned pin without warning.
- **Debug tooling suggestion:** rather than reserving a UART pin pair for serial debug output, consider adding a third interface (USB CDC serial) inside the same composite USB descriptor alongside HID and UAC2. TinyUSB supports multi-interface composite devices, and this avoids consuming any GPIO for debug at all. Worth deciding during Milestone 1–2.

**Known board-level limitation (informational, not currently relevant):** Seeed's own documentation states the XIAO RP2040 cannot be connected to USB-C while a LiPo battery is also connected, for safety reasons. Not applicable to this design (bus-powered only, no battery), but worth knowing if a future revision considers battery backup.

---

## 9. USB device requirements

1. Device must enumerate as a **composite USB device** combining:
   - A USB HID keyboard interface (boot or report protocol)
   - A USB Audio Class 2.0 (UAC2) microphone interface
   - Combined properly via an **Interface Association Descriptor (IAD)** so the host OS binds its native HID driver to one function and its native audio driver to the other, without any custom driver.
2. Zero driver installation required on any tested OS — this is the core hard requirement from Message 1 and the highest-risk item in the whole project (see Section 13).
3. **USB Full-Speed (12 Mbps)** is sufficient bandwidth for mono or stereo 48kHz/16-bit audio; no need to target High-Speed USB.
4. Device is **bus-powered only** — no self-powered mode, draws power entirely from the host's VBUS over the single USB-C connector.
5. Reference firmware starting points (TinyUSB, bundled with the Pico SDK):
   - `uac2_headset` example
   - `audio_4_channel_mic` example
   - Both should be studied for descriptor structure before writing a custom composite descriptor.
6. **Firmware behavior for the privacy-preserving gating pattern** (see Locked Decision 6): the UAC2 interface should remain enumerated continuously once the device is plugged in. The push-to-talk button and always-stream switch control, at the firmware level, whether real ADC/PIO-sourced samples or silence are written into the isochronous IN endpoint's data. This should never involve tearing down and re-establishing the USB Audio interface.

---

## 10. Claude Code keybinding reference (verified against live docs at time of writing)

**Caveat up front, and this is important: Claude Code ships weekly, and the specifics below were verified via live documentation search at conversation time. Before finalizing the firmware's keystroke map, re-check current behavior at https://code.claude.com/docs/en/permission-modes and https://docs.claude.com — do not assume these bindings are still current by the time firmware is written, especially if there's been a gap of weeks or more.**

### Per-action approval prompt
The prompt shown for individual tool actions (Bash commands, file edits, web fetches, etc.) presents three numbered choices, with the first pre-highlighted as default:
1. Approve once.
2. Approve **and** add a persistent "don't ask again" rule (scope — local project / user / project — has varied across versions; check current behavior).
3. Reject and give Claude Code different instructions — this option is also reachable via the Escape key.

**Resulting keystrokes to emit:**
- Approve once → `Enter` (works because option 1 is the highlighted default) or literal `1`
- Approve + remember → `2`
- Reject → `Esc` (or `3`)

### Permission-mode cycling (separate from the above)
`Shift+Tab` cycles the *session-wide* autonomy mode: `default` → `acceptEdits` → `auto` (only appears if the account is eligible for auto mode) → `plan`. This is a different control from the per-action approve/reject prompt — it changes how many future prompts will even appear, rather than answering one prompt.

### Plan-mode approval (distinct multi-option menu, not simple yes/no)
When Claude Code has finished plan-mode research and proposes a plan, the prompt is a menu with multiple named options (approve-and-switch-to-auto, approve-and-accept-edits, approve-for-manual-review, or keep refining the plan) rather than a binary yes/no. Selection is by number key, with `Enter` selecting whichever option is currently the default. There's also a documented `Ctrl+G` shortcut to open the proposed plan in the user's default text editor for manual edits before proceeding. **No dedicated hardware button currently targets this menu** — see Open Question OQ7.

### Durability recommendation (see OQ3)
Claude Code also ships a formal **user-configurable keybinding system**: running `/keybindings` inside a session generates (or opens) `~/.claude/keybindings.json`, where individual actions in named "contexts" can be bound to specific key combinations, validated against a published JSON schema. Rather than hardcoding the current default prompt keys into this device's firmware, consider having the firmware target a small set of custom, unambiguous bindings that Geoff defines once in that config file — this would insulate the hardware from future changes to Claude Code's own defaults. This is a genuine open decision (OQ3), not a locked choice.

---

## 11. Firmware design requirements summary

- Language/stack: see OQ1 (unresolved).
- USB stack: TinyUSB (whichever wrapper — raw Pico SDK or Arduino core).
- Composite descriptor: HID keyboard interface + UAC2 microphone interface + IAD, optionally + USB CDC for debug (see Section 8 debug tooling note).
- Audio path: PIO-based I2S receive (no native I2S peripheral on RP2040) → gating logic (real samples vs. silence based on button/switch state) → UAC2 isochronous IN FIFO.
- Button/switch handling: internal pull-ups, active-low, software debounce, mapped per Section 8's pin table to the HID keystrokes in Section 10.
- Status indication: onboard NeoPixel/RGB LED reflects live mic-streaming state (remember the active-low LED-enable quirk noted in Section 8).
- Known component-level firmware risk: the SPH0645 mic's I2S output has documented quirks — it's left-justified with a bit-alignment offset from a "textbook" I2S stream, and it carries a DC offset that typically needs a high-pass/DC-blocking filter in firmware to avoid audible artifacts. Budget real debugging time for this at Milestone 5; verify against the current SPH0645 datasheet and community example code before assuming a specific fix.

---

## 12. Work breakdown / milestone plan

Work in this order. Each milestone has a hard pass/fail gate — do not proceed past a milestone whose gate hasn't been met, and do not skip ahead because a later milestone seems easier. The composite-USB-device milestone (M4) is the single highest-risk step in the whole project and should be treated as such.

### M1 — Toolchain bring-up
- Resolve OQ1 (firmware toolchain) if not already resolved.
- Install the chosen toolchain.
- Flash the XIAO RP2040 via its BOOTSEL bootloader (hold the BOOT button while connecting USB-C → board appears as a USB mass-storage drive → drag on a `.uf2` file) with a minimal program that blinks the onboard LED.
- Remember the active-low LED convention noted in Section 8.
- **Gate:** a self-built UF2 flashes successfully and the LED blinks at an interval set in your own source code (not a stock example you haven't modified).

### M2 — HID keyboard, standalone
- Build a minimal TinyUSB HID keyboard descriptor. No audio interface yet.
- Emit one test keystroke via a timer or a simple debug trigger.
- **Gate:** device enumerates as a standard keyboard on macOS with **zero driver prompts**, and the test keystroke lands in a text field.

### M3 — UAC2 microphone, standalone, synthetic audio
- Build a minimal TinyUSB UAC2 descriptor for a microphone-input-only device (mono or stereo, 48kHz/16-bit). No HID yet.
- Fill the isochronous IN FIFO with a firmware-generated sine wave — **no physical microphone wired yet.**
- **Gate:** device enumerates as an audio input device on macOS with zero driver prompts, and the tone is recordable in QuickTime or Audacity.

### M4 — Composite device: HID + UAC2 together — **highest-risk milestone**
- Merge M2 and M3 into a single composite descriptor using a correctly structured Interface Association Descriptor.
- **Gate:** a single physical device plugged into one USB-C port simultaneously shows up as *both* a keyboard and a microphone, with zero driver installation, on macOS at minimum (see OQ6 for whether Windows/Linux validation is in scope). This is the point where the core "single peripheral, both keyboard and mic, no drivers" requirement from Message 1 is proven at the protocol level.

### M5 — Real microphone integration
- Resolve OQ2 (purchase the mic breakout) if not already resolved.
- Breadboard-wire the mic per the Section 8 pin table (BCLK→D4, LRCLK→D5, SD→D3, SEL→GND).
- Implement PIO-based I2S receive on the RP2040 (there is no hardware I2S peripheral — this must go through PIO).
- Replace the synthetic tone from M3 with real mic samples.
- Address the SPH0645 bit-alignment/DC-offset quirks noted in Section 11.
- **Gate:** a recorded sample is intelligible speech, not noise, silence, or garbled audio.

### M6 — Buttons, switch, gating logic, and status LED
- Wire all 5 physical controls (push-to-talk, always-stream switch, and the 3 keystroke buttons... **note: Section 8's table has 4 keystroke buttons, not 3** — approve/approve+remember/reject/mode-toggle — reconcile this against Geoff's original "three buttons" framing per the note at the end of Section 2, and confirm the final control count with Geoff if it hasn't already been settled) per the Section 8 pin map, with internal pull-ups and software debounce.
- Implement push-to-talk gating: samples flow only while the button is held; released, silence flows (see OQ5 for exact silence behavior).
- Implement always-stream latch behavior, including the both-active edge case (OQ4).
- Wire the 4 keystroke buttons to their HID outputs per Section 10, resolving OQ3 (default-keys vs. custom keybindings.json) before finalizing.
- Drive the onboard RGB LED to reflect live mic state.
- **Gate:** a full end-to-end test inside a real Claude Code session — talk on push-to-talk and confirm the audio is received correctly by whatever app/service Claude Code routes it through; press each keystroke button and confirm the correct action occurs in a terminal that has focus.

### M7 — Polish and lock for PCB handoff
- Finalize debounce timings and the always-stream/push-to-talk interaction.
- Decide and implement key-repeat behavior (or explicit non-repeat) for the keystroke buttons.
- Freeze the pin map, parts list, and firmware behavior as the locked baseline.
- **Only after this gate is met:** begin custom PCB layout. PCB design is explicitly out of scope for this work breakdown — it is Geoff's stated next phase (Section 3, Locked Decision 4) and should be spec'd separately once M7 is reached.

---

## 13. Known technical risks

1. **UAC2 composite-descriptor firmware (M4)** is the single highest-risk item in the project — this was flagged as "the only genuinely fiddly bit" in the original design exploration. Everything else (buttons, I2S mic reads) is comparatively well-trodden ground.
2. **SPH0645 I2S output quirks** (bit alignment, DC offset) — budget real debugging time; don't assume a naive I2S read will produce clean audio.
3. **Claude Code keybinding drift** — the product ships weekly; hardcoded default keys may silently stop matching the live UI. See OQ3 and Section 10's durability recommendation.
4. **Board variant ambiguity** — don't assume the ordered XIAO RP2040 is breadboard-ready out of the box; confirm per Section 4 the moment it arrives.
5. **Two blocking open decisions gate the very first milestone**: OQ1 (toolchain) must be resolved before M1 can start at all.
6. **Scope of "no drivers"** — the hard requirement doesn't specify which OS(es); don't over- or under-invest in cross-platform testing without checking OQ6 with Geoff first.

---

## 14. Deferred: custom PCB phase (not in scope for current work)

Once the breadboard design is locked (M7 gate), Geoff's stated plan is a custom PCB — either carrying the XIAO RP2040 module itself (its castellated edge pads and "no components on the back" design mean it's meant to be reflow- or hand-soldered directly onto a carrier board) or, if the UAC2 firmware proves genuinely infeasible on the RP2040 module, a fallback path explored earlier in the design conversation using dedicated audio-class silicon instead of firmware-implemented USB Audio:

- Bare-chip alternative silicon (if ever needed): Raspberry Pi RP2354B — has 2MB of stacked flash on-package, avoiding an external QSPI flash chip. https://thepihut.com/products/raspberry-pi-rp2354b-microcontroller (also available via LCSC: https://www.lcsc.com/product-detail/C39843328.html)
- Hardware-audio-codec fallback (if firmware UAC2 proves too costly): TI PCM2902C class-compliant USB stereo audio codec (https://www.ti.com/product/PCM2902C) paired with a USB hub IC (e.g. Microchip USB2422) to combine it with a separate HID microcontroller behind one port. This path trades firmware risk for an analog mic input (rather than the digital I2S mic used in the current plan) and added board complexity — it is a fallback, not the current direction, and should only be revisited if M4 proves unworkable on the RP2040.

**This entire section is deprioritized and informational only** — the current locked path is the XIAO RP2040 module handling both HID and UAC2 in firmware. Do not start PCB or alternative-silicon work until Section 12's M7 gate is reached and Geoff explicitly asks for it.

---

## 15. Reference links (consolidated)

- Seeed XIAO RP2040 (headers): https://www.seeedstudio.com/XIAO-RP2040-v1-0-p-5026.html
- Seeed XIAO RP2040 (pre-soldered): https://www.seeedstudio.com/Seeed-Studio-XIAO-RP2040-Pre-Soldered-p-6333.html
- Seeed XIAO RP2040 wiki: https://wiki.seeedstudio.com/XIAO-RP2040/
- TinyGo XIAO RP2040 pin/peripheral reference: https://tinygo.org/docs/reference/microcontrollers/machine/xiao-rp2040/
- Seeed XIAO Expansion Base (prototyping aid, optional): https://www.seeedstudio.com/Seeeduino-XIAO-Expansion-board-p-4746.html
- Adafruit SPH0645 I2S MEMS mic: https://www.adafruit.com/product/3421
- Adafruit ICS-43434 I2S MEMS mic (discontinued per vendor): https://www.adafruit.com/product/6049
- Claude Code permission modes docs: https://code.claude.com/docs/en/permission-modes
- Claude Code approval-prompt UI reference (GitHub issue with live examples): https://github.com/anthropics/claude-code/issues/11073
- Anthropic engineering blog on Claude Code auto mode: https://www.anthropic.com/engineering/claude-code-auto-mode
- (Deferred/fallback) RP2354B: https://thepihut.com/products/raspberry-pi-rp2354b-microcontroller
- (Deferred/fallback) TI PCM2902C: https://www.ti.com/product/PCM2902C

---

*End of spec. If anything in this document conflicts with a direct instruction from Geoff, his instruction wins — flag the conflict rather than silently resolving it.*
