"""Single source of dimensional truth for the carrier PCB, enclosure, and
3D mockup. Every consumer (PCB generator, enclosure CAD, mockup assembly)
imports from here — never re-declare a dimension locally.

All dimensions in millimetres. Origin convention for board-space coordinates:
X=0 at board centreline (+X right when looking at the front face),
Y=0 at board top edge (+Y downward toward the USB-C end).

Dimension sources are noted per block. Anything marked VERIFY must be
checked against the current datasheet before ordering fabrication — these
values are correct per the datasheets as known at design time, but the
project convention (docs/SPEC.md §0) is to re-verify time-sensitive facts.
"""

# --------------------------------------------------------------------------
# Seeed Studio XIAO RP2040 module
# Source: Seeed wiki + XIAO RP2040 dimension drawing.
# --------------------------------------------------------------------------
XIAO_L = 21.0          # module PCB length (along USB axis)
XIAO_W = 17.8          # module PCB width
XIAO_PCB_T = 1.2       # module PCB thickness
XIAO_PAD_PITCH = 2.54  # castellated edge pads, 7 per long side
XIAO_PADS_PER_SIDE = 7
XIAO_USB_W = 8.94      # USB-C connector width
XIAO_USB_H = 3.26      # USB-C connector height (above module PCB top)
XIAO_USB_OVERHANG = 1.3   # connector protrusion past module PCB edge
XIAO_TOP_CLEARANCE = 4.6  # tallest point above carrier when soldered flat
                          # (module PCB + USB-C shell), VERIFY on real board

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
# Knowles SPH0645LM4H-B I2S MEMS microphone (bare part, bottom-port)
# Source: Knowles SPH0645LM4H-B datasheet.
# --------------------------------------------------------------------------
MIC_L = 3.5
MIC_W = 2.65
MIC_H = 0.98
MIC_PORT_PCB_HOLE = 0.7   # acoustic port hole through carrier PCB
# Bottom-port: mic is mounted on the BACK of the carrier; sound enters
# through the PCB hole from the front side.

# --------------------------------------------------------------------------
# C&K PCM12SMTR right-angle SMT slide switch (always-stream latch)
# Actuator extends past the PCB edge -> pokes through the enclosure side
# wall, per PHYSICAL_DESIGN_SPEC §2.3 (latch on the side of the shell).
# Source: C&K PCM12 series datasheet. VERIFY exact body dims before fab.
# --------------------------------------------------------------------------
SLIDE_BODY_L = 8.7        # along PCB edge
SLIDE_BODY_W = 3.6        # into the board
SLIDE_BODY_H = 3.4        # above PCB
SLIDE_KNOB = 1.5          # knob square section
SLIDE_KNOB_EXT = 2.4      # knob protrusion past PCB edge at mid-throw
SLIDE_TRAVEL = 2.0        # end-to-end actuator travel

# --------------------------------------------------------------------------
# WS2812B (5050) addressable status LED, on carrier top edge (D10/GPIO3)
# --------------------------------------------------------------------------
LED_SIZE = 5.0
LED_H = 1.6
LED_WINDOW = 2.5          # enclosure light hole dia

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
MIC_POS = (0.0, 6.5)          # top centre, back side, port thru PCB
LED_POS = (14.0, 8.0)         # top right, front side
SLIDE_POS_Y = 16.0            # right board edge, actuator past edge
XIAO_POS_Y = 92.5             # module centre; USB-C flush w/ bottom edge

# --------------------------------------------------------------------------
# Enclosure (FDM, split shell: front + back)
# --------------------------------------------------------------------------
WALL = 2.0                # min wall for FDM
SHELL_CLEAR = 0.6         # PCB-to-inner-wall lateral clearance
FRONT_GAP = 0.5           # switch housing top to front-wall inner face
BACK_GAP = 3.2            # PCB back clearance (switch pins 2.65 + margin)
SHELL_CORNER_R = 6.0      # outer corner radius (hand feel)
CAP_HOLE_CLEAR = 0.5      # per-side clearance around keycaps in front face

# Derived overall envelope
SHELL_W = PCB_W + 2 * (SHELL_CLEAR + WALL)                    # ≈ 49.2
SHELL_L = PCB_L + 2 * (SHELL_CLEAR + WALL)                    # ≈ 109.2
SHELL_T = (WALL + BACK_GAP + PCB_T + CHOC_H_ABOVE_PCB
           + FRONT_GAP + WALL)                                # ≈ 14.3

BOSS_D = 5.0              # screw boss dia (M2 self-tapping)
BOSS_PILOT = 1.7          # pilot hole for M2 self-tap
MIC_SHELL_HOLE = 1.5      # front-face acoustic hole dia
USB_CUT_W = XIAO_USB_W + 1.6   # bottom-wall USB-C opening
USB_CUT_H = XIAO_USB_H + 1.2
SLIDE_SLOT_L = SLIDE_BODY_L - 1.0  # side-wall slot for latch knob
SLIDE_SLOT_W = SLIDE_KNOB + 1.2
