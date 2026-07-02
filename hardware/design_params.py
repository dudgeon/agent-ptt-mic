"""Single source of dimensional truth for the carrier PCB, enclosure, and
3D mockup. Every consumer (PCB generator, enclosure CAD, mockup assembly)
imports from here — never re-declare a dimension locally.

All dimensions in millimetres. Origin convention for board-space coordinates:
X=0 at board centreline (+X right when looking at the front face),
Y=0 at board top edge (+Y downward toward the USB-C end).

Dimension sources are noted per block. Anything marked VERIFY must be
checked against the current datasheet/physical part before ordering
fabrication — these values are correct per the datasheets as known at
design time, but the project convention (docs/SPEC.md §0) is to re-verify
time-sensitive facts.

Mounting revision (2026-07-02): the XIAO RP2040 Geoff ordered is the
PRE-SOLDERED variant (docs/SPEC.md §4) -- it arrives with 0.1" pin headers
already on it, not bare castellated edges meant for reflow onto a carrier.
Likewise the mic is a breakout MODULE (pin-header, like the original
breadboard-track SPH0645 breakout), not a bare SMD chip, and the status
LED is a plain THT LED, not an addressable SMD WS2812B. Net effect: the
whole carrier is now hand-iron-solderable, no reflow/hot-air anywhere --
at the cost of a notably thicker enclosure, since a header-mounted module
needs real standoff clearance instead of sitting flush.
"""

# --------------------------------------------------------------------------
# Seeed Studio XIAO RP2040 module -- PRE-SOLDERED variant (pin headers)
# Source: Seeed wiki pinout (X-Y pin spacing is a fixed module dimension,
# unchanged by header-vs-castellated). Header standoff/pin-length figures
# are typical-for-class estimates -- VERIFY against the physical board
# before finalizing enclosure thickness.
# --------------------------------------------------------------------------
XIAO_L = 21.0          # module PCB length (along USB axis)
XIAO_W = 17.8          # module PCB width
XIAO_PCB_T = 1.2       # module PCB thickness
XIAO_PAD_PITCH = 2.54  # header pin pitch, 7 per long side
XIAO_PADS_PER_SIDE = 7
XIAO_USB_W = 8.94      # USB-C connector width
XIAO_USB_H = 3.26      # USB-C connector height (above module top face)
XIAO_USB_OVERHANG = 1.3   # connector protrusion past module PCB edge

# Mounting: module sits on the carrier's BACK, pin-side facing the carrier.
# Its own presoldered header pins pass through 14 plated holes in the
# carrier and solder flush on the carrier's FRONT copper (a clear area near
# the bottom edge, away from the switch cluster) -- no separate header/
# socket part needed, and it's permanent rather than a swappable socket
# (simplest + thinnest of the two mounting options; a female-header socket
# would add another ~8.5mm of standoff for zero benefit at this quantity).
XIAO_HDR_ROW_SPACING = 16.4  # column-to-column (was col_x*2 in prior rev)
XIAO_MODULE_STANDOFF = 6.0   # VERIFY: gap from carrier back face to module
                             # PCB underside, bridged by the module's own
                             # presoldered pin legs
XIAO_TOTAL_DEPTH = (XIAO_MODULE_STANDOFF + XIAO_PCB_T + XIAO_USB_H)  # 10.46
                             # carrier back face -> outward tip of USB-C
                             # (component side, incl. USB-C, faces AWAY
                             # from the carrier, deeper into the back shell)

# --------------------------------------------------------------------------
# Kailh Choc V1 (PG1350) low-profile mechanical keyswitch
# Source: Kailh PG1350 datasheet drawing; footprint cross-checked against
# the common community footprint (ai03 / keebio style).
# --------------------------------------------------------------------------
CHOC_BODY = 15.0          # top flange, square
CHOC_BODY_UNDER = 13.8    # lower housing, square (also plate-cutout size)
CHOC_H_ABOVE_PCB = 5.0    # housing top above PCB (excl. stem)
CHOC_STEM_H = 3.0         # stem above housing at rest
CHOC_PIN_DEPTH = 2.65     # pins/posts below PCB bottom
CHOC_STEM_HOLE = 3.4      # centre locating post hole dia
CHOC_POST_HOLE = 1.9      # side locating post hole dia
CHOC_POST_X = 5.5         # side posts at (±5.5, 0)
CHOC_PIN1 = (0.0, -5.9)   # switch contact 1 (x, y) rel. to switch centre
CHOC_PIN2 = (5.0, -3.8)   # switch contact 2  — VERIFY handed variant
CHOC_PIN_HOLE = 1.2       # contact pin hole dia (plated)

# MBK / Choc-profile keycap
CAP_W = 17.5              # 1u Choc cap, X
CAP_D = 16.5              # 1u Choc cap, Y
CAP_H = 3.0               # cap slab thickness
CAP_TOP_ABOVE_PCB = 10.8  # cap top surface above PCB (switch + cap stack)

KEY_PITCH_X = 18.0        # Choc-standard key spacing
KEY_PITCH_Y = 17.0

# --------------------------------------------------------------------------
# I2S MEMS mic BREAKOUT MODULE (e.g. Adafruit SPH0645, PID 3421) -- same
# part family as the breadboard-track BOM (docs/SPEC.md OQ2), not the bare
# SMD chip used in the previous PCB revision. Dimensions confirmed 2026-07-02
# against Adafruit's own product listing (adafruit.com/product/3421,
# "Technical Details": "Product Dimensions: 16.7mm x 12.7mm x 1.8mm") --
# live-verified, no longer an estimate.
# --------------------------------------------------------------------------
MIC_BRK_L = 16.7          # breakout PCB length (confirmed, Adafruit listing)
MIC_BRK_W = 12.7          # breakout PCB width (confirmed, Adafruit listing)
MIC_BRK_H = 1.8           # breakout PCB + capsule (confirmed, Adafruit listing)
MIC_BRK_PINS = 6          # 3V, GND, BCLK, DOUT, LRCL, SEL -- matches the
                          # breadboard-track wiring in docs/SPEC.md §8
MIC_BRK_PIN_PITCH = 2.54
MIC_BRK_STANDOFF = 3.0    # header standoff above carrier front face

# --------------------------------------------------------------------------
# C&K PCM12SMTR right-angle SMT slide switch (always-stream latch)
# Actuator extends past the PCB edge -> pokes through the enclosure side
# wall, per PHYSICAL_DESIGN_SPEC §2.3 (latch on the side of the shell).
# Source: C&K PCM12 series datasheet. VERIFY exact body dims before fab.
# Kept as SMD: it's ordinary hand-solder-friendly gull-wing pads, not a
# reflow-only part like the mic chip was -- no reason to swap it out.
# --------------------------------------------------------------------------
SLIDE_BODY_L = 8.7        # along PCB edge
SLIDE_BODY_W = 3.6        # into the board
SLIDE_BODY_H = 3.4        # above PCB
SLIDE_KNOB = 1.5          # knob square section
SLIDE_KNOB_EXT = 2.4      # knob protrusion past PCB edge at mid-throw
SLIDE_TRAVEL = 2.0        # end-to-end actuator travel

# --------------------------------------------------------------------------
# Addressable RGB status LED (WS2812B/SK6812-style, 5050 package), front
# side, D10/GPIO3 -- v2.1 revision (2026-07-02b).
#
# Geoff asked for a true RGB status LED ("for future status options") but
# said it doesn't need to be addressable. It turns out the pin budget
# forces the addressable choice anyway: a genuine discrete RGB LED needs 3
# independent GPIOs (separate R/G/B anodes), and docs/SPEC.md §8's locked
# pin map leaves only 2 spares (D9, D10) after the 9 assigned signals --
# one short. An addressable LED needs just 1 data pin for full RGB, which
# fits the existing D10 allocation exactly. Firmware only needs to drive
# solid colors (per Geoff's "doesn't need to be addressable" -- no fancy
# animation requirement), it just has to speak the WS2812 protocol to do
# even that, since that's how the color is set on this class of part.
# Still hand-solderable: 5050 pads are large gull-wing/castellated-corner
# pads reachable with a fine-tip iron, not a reflow-only part like the
# bare mic chip was in v1.
# --------------------------------------------------------------------------
LED_SIZE = 5.0            # 5050 package, square
LED_H = 1.6               # package height above PCB
LED_WINDOW = 3.4          # enclosure light window dia
RES_THT_LEN = 6.5         # axial resistor body length (1/4W) -- data-line
RES_THT_DIA = 2.2         # series resistor (signal integrity, not current-
RES_THT_LEAD_SPACING = 10.0  # limiting -- WS2812 draws its own current)

# --------------------------------------------------------------------------
# Carrier PCB
# --------------------------------------------------------------------------
PCB_W = 44.0
PCB_L = 104.0
PCB_T = 1.6
PCB_CORNER_R = 3.0
PCB_HOLE_D = 2.2          # M2 mounting holes
# mounting hole centres, (x, y) in board space:
PCB_HOLES = [(-18.5, 4.0), (18.5, 4.0), (-18.5, 94.0), (18.5, 94.0)]

# Control positions (x, y) in board space, front side.
# 2x2 keystroke cluster + PTT below it (thumb rest), per the layout
# decision recorded in PHYSICAL_DESIGN_SPEC §2.3 (as amended this session).
KEY_POS = {
    "approve":  (-KEY_PITCH_X / 2, 30.0),   # top-left     -> Enter
    "remember": ( KEY_PITCH_X / 2, 30.0),   # top-right    -> '2'
    "reject":   (-KEY_PITCH_X / 2, 47.0),   # bottom-left  -> Esc
    "mode":     ( KEY_PITCH_X / 2, 47.0),   # bottom-right -> Shift+Tab
    "ptt":      (0.0, 68.0),                # bottom-centre, thumb rest
}
MIC_POS = (0.0, 10.0)         # top centre, front side (breakout module)
LED_POS = (14.0, 8.0)         # top right, front side
SLIDE_POS_Y = 16.0            # right board edge, actuator past edge
XIAO_POS_Y = 92.5             # module centre, BACK side; USB-C flush w/
                              # bottom edge, facing away into the back shell

# --------------------------------------------------------------------------
# Enclosure (FDM, split shell: front + back)
# --------------------------------------------------------------------------
WALL = 2.0                # min wall for FDM
SHELL_CLEAR = 0.6         # PCB-to-inner-wall lateral clearance
FRONT_GAP = 0.5           # switch housing top to front-wall inner face
# Back clearance must fit the XIAO module hanging off the back via its own
# header pins (XIAO_TOTAL_DEPTH ~= 10.5mm) plus margin -- this is the
# dimension that grew substantially from the flush-SMD-mount revision
# (was 3.2mm there; the module alone now needs ~10.5mm).
BACK_GAP = 11.5
SHELL_CORNER_R = 6.0      # outer corner radius (hand feel)
CAP_HOLE_CLEAR = 0.5      # per-side clearance around keycaps in front face

# Derived overall envelope
SHELL_W = PCB_W + 2 * (SHELL_CLEAR + WALL)                    # ≈ 49.2
SHELL_L = PCB_L + 2 * (SHELL_CLEAR + WALL)                    # ≈ 109.2
SHELL_T = (WALL + BACK_GAP + PCB_T + CHOC_H_ABOVE_PCB
           + FRONT_GAP + WALL)                                # ≈ 22.6

BOSS_D = 5.0              # screw boss dia (M2 self-tapping)
BOSS_PILOT = 1.7          # pilot hole for M2 self-tap
MIC_SHELL_CLEAR = 0.8     # front-face window clearance around mic breakout
USB_CUT_W = XIAO_USB_W + 1.6   # bottom-wall USB-C opening
USB_CUT_H = XIAO_USB_H + 1.2
SLIDE_SLOT_L = SLIDE_BODY_L - 1.0  # side-wall slot for latch knob
SLIDE_SLOT_W = SLIDE_KNOB + 1.2
