"""Generate the carrier-board KiCad PCB (`companion_carrier.kicad_pcb`).

Produces a netlisted, fully-placed 2-layer board: XIAO RP2040 module
(pre-soldered/header variant -- through-hole pins, mounted on the BACK),
5x Kailh Choc V1 keyswitches, PCM12SMTR side-actuated latch slide, an I2S
mic BREAKOUT MODULE (header-mounted, front side -- not a bare SMD chip),
a plain THT status LED + series resistor, THT decoupling passives,
mounting holes, board outline, and GND zones on both copper layers.

2026-07-02 revision: every active part on this board is now a
through-hole / header-mount component, hand-solderable with a plain iron
-- no reflow or hot-air needed anywhere (see hardware/BOM.md and
docs/PHYSICAL_DESIGN_SPEC.md for why: the XIAO Geoff ordered is the
pre-soldered/header SKU, and the mic and LED were swapped off bare-SMD/
addressable parts to match).

Deliberately NOT routed: signal traces are left to an interactive KiCad
session where DRC runs live (see README.md in this directory). Every net
is attached to its pads, so the ratsnest is complete when opened.

Run from the repo root:  python3 hardware/pcb/generate_pcb.py
"""

import math
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
import design_params as P  # noqa: E402

from kiutils.board import Board  # noqa: E402
from kiutils.footprint import Footprint, Pad, DrillDefinition, Attributes  # noqa: E402
from kiutils.items.common import Net, Position, Effects, Font  # noqa: E402
from kiutils.items.gritems import GrLine, GrArc  # noqa: E402
from kiutils.items.fpitems import FpText, FpLine, FpCircle  # noqa: E402
from kiutils.items.zones import Zone, FillSettings, Hatch, ZonePolygon  # noqa: E402
from kiutils.items.brditems import LayerToken  # noqa: E402

# Board-space -> sheet-space offset (keeps the board away from the sheet origin)
OX, OY = 60.0, 30.0


def pos(x, y, angle=None):
    """Board space (x from centreline, y from top edge) -> KiCad sheet mm."""
    return Position(X=round(OX + x, 3), Y=round(OY + y, 3), angle=angle)


# --------------------------------------------------------------------------
# Nets
# --------------------------------------------------------------------------
NET_NAMES = [
    "", "GND", "3V3", "5V",
    "PTT", "LATCH", "KEY_APPROVE", "KEY_REMEMBER", "KEY_REJECT", "KEY_MODE",
    "I2S_SD", "I2S_BCLK", "I2S_LRCLK", "LED_DATA", "LED_A", "SPARE_D9",
]
NETS = {name: Net(number=i, name=name) for i, name in enumerate(NET_NAMES)}


def net(name):
    return Net(number=NETS[name].number, name=name)


# --------------------------------------------------------------------------
# Pad helpers
# --------------------------------------------------------------------------
def smd_pad(number, x, y, w, h, netname=None, layer="F.Cu"):
    mask = "F.Mask" if layer == "F.Cu" else "B.Mask"
    paste = "F.Paste" if layer == "F.Cu" else "B.Paste"
    return Pad(
        number=str(number), type="smd", shape="roundrect",
        position=Position(X=round(x, 3), Y=round(y, 3)),
        size=Position(X=w, Y=h), layers=[layer, mask, paste],
        roundrectRatio=0.25,
        net=net(netname) if netname else None,
    )


def tht_pad(number, x, y, pad_d, drill_d, netname=None):
    return Pad(
        number=str(number), type="thru_hole", shape="circle",
        position=Position(X=round(x, 3), Y=round(y, 3)),
        size=Position(X=pad_d, Y=pad_d),
        drill=DrillDefinition(diameter=drill_d),
        layers=["*.Cu", "*.Mask"],
        net=net(netname) if netname else None,
    )


def npth(x, y, drill_d):
    return Pad(
        number="", type="np_thru_hole", shape="circle",
        position=Position(X=round(x, 3), Y=round(y, 3)),
        size=Position(X=drill_d, Y=drill_d),
        drill=DrillDefinition(diameter=drill_d),
        layers=["*.Cu", "*.Mask"],
    )


def ref_text(ref, y=-3.0, layer="F.SilkS", hide=False):
    return FpText(
        type="reference", text=ref, position=Position(X=0, Y=y),
        layer=layer, hide=hide,
        effects=Effects(font=Font(height=0.8, width=0.8, thickness=0.12)),
    )


def fp(name, ref, at, pads, extra_items=None, layer="F.Cu", smd=True):
    f = Footprint(
        libraryNickname="carrier", entryName=name,
        version="20240108", generator="generate_pcb.py",
        layer=layer, position=at,
        attributes=Attributes(type="smd" if smd else "through_hole"),
        pads=pads,
        graphicItems=[ref_text(ref, layer="F.SilkS" if layer == "F.Cu" else "B.SilkS")]
        + (extra_items or []),
    )
    return f


def header_row(prefix, cx, cy0, count, pitch, nets, pad_d=1.8, drill_d=1.0,
               vertical=True):
    """A single row of THT header pins -- used for both the XIAO module's
    presoldered pins (pushed through the carrier and soldered) and the mic
    breakout's header."""
    pads = []
    for i in range(count):
        y = cy0 + i * pitch if vertical else cy0
        x = cx if vertical else cx + i * pitch
        pads.append(tht_pad(f"{prefix}{i+1}", x, y, pad_d, drill_d, nets[i]))
    return pads


def outline_lines(w, h, layer="F.SilkS"):
    x, y = w / 2, h / 2
    pts = [(-x, -y), (x, -y), (x, y), (-x, y), (-x, -y)]
    return [
        FpLine(start=Position(X=pts[i][0], Y=pts[i][1]),
               end=Position(X=pts[i + 1][0], Y=pts[i + 1][1]),
               layer=layer, width=0.12)
        for i in range(4)
    ]


# --------------------------------------------------------------------------
# Footprints
# --------------------------------------------------------------------------
def xiao_rp2040(ref, cx, cy):
    """XIAO module -- PRE-SOLDERED/header SKU, mounted on the carrier's
    BACK. Its own presoldered header pins pass through 14 plated holes and
    solder flush on the carrier's front copper; no separate header/socket
    part needed (see design_params.py XIAO_MODULE_STANDOFF). Component
    side (RP2040, USB-C) faces away from the carrier, into the back shell
    cavity -- USB-C points to +Y (board bottom edge).

    Pin map viewed from the BACK (component side facing away): the module
    is rotated 180 deg from Seeed's usual USB-up/top-view drawing, so the
    columns swap/flip same as the prior flush-mount revision.
    VERIFY pad geometry against Seeed's official footprint before fab.
    """
    pitch, col_x = P.XIAO_PAD_PITCH, P.XIAO_HDR_ROW_SPACING / 2
    left = ["KEY_REJECT", "KEY_MODE", "SPARE_D9", "LED_DATA", "3V3", "GND", "5V"]
    right = ["KEY_REMEMBER", "I2S_LRCLK", "I2S_BCLK", "I2S_SD",
             "KEY_APPROVE", "LATCH", "PTT"]
    y0 = -pitch * 3
    pads = (header_row("L", -col_x, y0, 7, pitch, left)
            + header_row("R", col_x, y0, 7, pitch, right))
    body = outline_lines(P.XIAO_W, P.XIAO_L, layer="B.SilkS")
    usb = outline_lines(P.XIAO_USB_W, 7.35, layer="B.SilkS")
    for line in usb:
        line.start.Y += P.XIAO_L / 2 - 7.35 / 2 + P.XIAO_USB_OVERHANG
        line.end.Y += P.XIAO_L / 2 - 7.35 / 2 + P.XIAO_USB_OVERHANG
    return fp("XIAO-RP2040_preSoldered_header", ref, pos(cx, cy), pads,
              layer="B.Cu", smd=False,
              extra_items=body + usb + [
                  FpText(type="user", text="USB-C v (hangs off back)",
                         layer="B.SilkS",
                         position=Position(X=0, Y=P.XIAO_L / 2 - 2),
                         effects=Effects(font=Font(height=0.7, width=0.7,
                                                   thickness=0.11)))])


def choc_v1(ref, cx, cy, netname):
    """Kailh Choc V1 (PG1350). Contacts: pin1 -> GPIO net, pin2 -> GND."""
    pads = [
        npth(0, 0, P.CHOC_STEM_HOLE),
        npth(-P.CHOC_POST_X, 0, P.CHOC_POST_HOLE),
        npth(P.CHOC_POST_X, 0, P.CHOC_POST_HOLE),
        tht_pad(1, P.CHOC_PIN1[0], P.CHOC_PIN1[1], 2.2, P.CHOC_PIN_HOLE, netname),
        tht_pad(2, P.CHOC_PIN2[0], P.CHOC_PIN2[1], 2.2, P.CHOC_PIN_HOLE, "GND"),
    ]
    body = outline_lines(P.CHOC_BODY, P.CHOC_BODY)
    cap = outline_lines(P.CAP_W, P.CAP_D, layer="F.Fab")
    return fp("Kailh_Choc_V1", ref, pos(cx, cy), pads,
              extra_items=body + cap, smd=False)


def slide_pcm12(ref, cx, cy):
    """C&K PCM12SMTR, right-angle SMT; actuator toward +X past board edge.

    Terminals face -X (into the board). VERIFY land pattern vs datasheet.
    """
    pads = [
        smd_pad(1, -2.4, -2.5, 1.6, 1.0, "LATCH"),
        smd_pad(2, -2.4, 0.0, 1.6, 1.0, "GND"),
        smd_pad(3, -2.4, 2.5, 1.6, 1.0, None),
        smd_pad("MP1", 1.2, -3.6, 1.8, 1.4, None),
        smd_pad("MP2", 1.2, 3.6, 1.8, 1.4, None),
    ]
    body = outline_lines(P.SLIDE_BODY_W, P.SLIDE_BODY_L)
    return fp("CK_PCM12SMTR", ref, pos(cx, cy), pads, extra_items=body)


def mic_breakout(ref, cx, cy):
    """I2S mic breakout MODULE (e.g. Adafruit SPH0645, PID 3421) -- a
    6-pin THT header, front side, standing off the carrier per
    MIC_BRK_STANDOFF. Same signal order as the breadboard-track wiring in
    docs/SPEC.md §8. Pin spacing/positions approximate -- VERIFY against
    the physical breakout before finalizing the enclosure window."""
    nets = ["3V3", "GND", "I2S_BCLK", "I2S_SD", "I2S_LRCLK", "GND"]  # SEL->GND
    n = P.MIC_BRK_PINS
    x0 = -(n - 1) * P.MIC_BRK_PIN_PITCH / 2
    pads = header_row("P", x0, 0.0, n, P.MIC_BRK_PIN_PITCH, nets,
                      vertical=False)
    body = outline_lines(P.MIC_BRK_L, P.MIC_BRK_W)
    return fp("MicBreakout_SPH0645-style", ref, pos(cx, cy), pads,
              extra_items=body, smd=False)


def led_tht(ref, cx, cy):
    """Plain 3mm THT LED. Anode (long lead) -> LED_A (via R1 from
    LED_DATA/GPIO3), cathode -> GND."""
    half = P.LED_THT_LEAD_SPACING / 2
    pads = [
        tht_pad(1, -half, 0, 1.4, 0.8, "LED_A"),   # anode
        tht_pad(2, half, 0, 1.4, 0.8, "GND"),      # cathode
    ]
    body = [FpCircle(center=Position(X=0, Y=0), end=Position(X=P.LED_THT_DIA / 2, Y=0),
                     layer="F.SilkS", width=0.12)]
    return fp("LED_3mm_THT", ref, pos(cx, cy), pads, extra_items=body, smd=False)


def passive_0603(ref, cx, cy, net1, net2, angle=None):
    pads = [
        smd_pad(1, -0.775, 0, 0.9, 1.0, net1),
        smd_pad(2, 0.775, 0, 0.9, 1.0, net2),
    ]
    return fp(f"R_C_0603", ref, pos(cx, cy, angle), pads,
              extra_items=outline_lines(1.6, 0.8, layer="F.Fab"))


def passive_tht(ref, cx, cy, net1, net2, spacing, pad_d=1.6, drill_d=0.8):
    """Generic THT passive (radial ceramic cap or axial resistor, formed
    to a vertical/radial lead spacing) -- hand-solderable, no fine-pitch
    tweezer work. Used for the decoupling caps and the LED series
    resistor so the whole board stays iron-only."""
    half = spacing / 2
    pads = [
        tht_pad(1, -half, 0, pad_d, drill_d, net1),
        tht_pad(2, half, 0, pad_d, drill_d, net2),
    ]
    return fp("THT_passive", ref, pos(cx, cy), pads,
              extra_items=outline_lines(spacing + 1.0, 2.0, layer="F.Fab"),
              smd=False)


def mount_hole(ref, cx, cy):
    return fp("MountingHole_M2", ref, pos(cx, cy), [npth(0, 0, P.PCB_HOLE_D)],
              smd=False)


# --------------------------------------------------------------------------
# Board outline (rounded rectangle on Edge.Cuts)
# --------------------------------------------------------------------------
def edge_cuts():
    w, h, r = P.PCB_W, P.PCB_L, P.PCB_CORNER_R
    x0, x1, y0, y1 = -w / 2, w / 2, 0.0, h
    items = []

    def gl(xa, ya, xb, yb):
        items.append(GrLine(start=pos(xa, ya), end=pos(xb, yb),
                            layer="Edge.Cuts", width=0.1))

    def garc(cx, cy, start, end):
        # KiCad arc: start point, mid point, end point (CCW start->end here
        # computed explicitly per corner).
        items.append(GrArc(start=start, mid=cy_mid(cx, cy, start, end),
                           end=end, layer="Edge.Cuts", width=0.1))

    def cy_mid(cx, cy, s, e):
        a0 = math.atan2(s.Y - (OY + cy), s.X - (OX + cx))
        a1 = math.atan2(e.Y - (OY + cy), e.X - (OX + cx))
        while a1 < a0:
            a1 += 2 * math.pi
        am = (a0 + a1) / 2
        return Position(X=round(OX + cx + r * math.cos(am), 4),
                        Y=round(OY + cy + r * math.sin(am), 4))

    gl(x0 + r, y0, x1 - r, y0)                       # top
    garc(x1 - r, y0 + r, pos(x1, y0 + r), pos(x1 - r, y0))
    gl(x1, y0 + r, x1, y1 - r)                       # right
    garc(x1 - r, y1 - r, pos(x1 - r, y1), pos(x1, y1 - r))
    gl(x1 - r, y1, x0 + r, y1)                       # bottom
    garc(x0 + r, y1 - r, pos(x0, y1 - r), pos(x0 + r, y1))
    gl(x0, y1 - r, x0, y0 + r)                       # left
    garc(x0 + r, y0 + r, pos(x0 + r, y0), pos(x0, y0 + r))
    return items


def gnd_zone(layer):
    m = 0.3
    w, h = P.PCB_W, P.PCB_L
    corners = [(-w / 2 + m, m), (w / 2 - m, m), (w / 2 - m, h - m),
               (-w / 2 + m, h - m)]
    poly = ZonePolygon(coordinates=[pos(x, y) for x, y in corners])
    return Zone(
        net=NETS["GND"].number, netName="GND", layers=[layer],
        name=f"GND_{layer}", hatch=Hatch(style="edge", pitch=0.5),
        clearance=0.4, minThickness=0.25,
        fillSettings=FillSettings(thermalGap=0.4, thermalBridgeWidth=0.4),
        polygons=[poly],
    )


# --------------------------------------------------------------------------
# Assemble board
# --------------------------------------------------------------------------
def build():
    board = Board.create_new()
    board.generator = "agent-ptt-mic/hardware/pcb/generate_pcb.py"
    board.nets = [NETS[n] for n in NET_NAMES]

    fps = []
    # Keyswitches (nets per docs/SPEC.md §8 + hardware/BOM.md)
    key_nets = {"approve": "KEY_APPROVE", "remember": "KEY_REMEMBER",
                "reject": "KEY_REJECT", "mode": "KEY_MODE", "ptt": "PTT"}
    sw_ref = {"approve": "SW1", "remember": "SW2", "reject": "SW3",
              "mode": "SW4", "ptt": "SW5"}
    for name, (x, y) in P.KEY_POS.items():
        fps.append(choc_v1(sw_ref[name], x, y, key_nets[name]))

    fps.append(slide_pcm12("SW6", P.PCB_W / 2 - P.SLIDE_BODY_W / 2,
                           P.SLIDE_POS_Y))
    fps.append(mic_breakout("MK1", *P.MIC_POS))
    fps.append(led_tht("D1", *P.LED_POS))
    fps.append(xiao_rp2040("U1", 0.0, P.XIAO_POS_Y))

    # Passives: all THT now (radial/axial leads) -- no fine-pitch SMD parts
    # left on the board at all. Mic decoupling near mic, LED resistor near
    # LED, bulk cap near the XIAO's 3V3 pins.
    fps.append(passive_tht("C1", -16.0, 20.0, "3V3", "GND", spacing=5.0))
    fps.append(passive_tht("C2", 9.0, 20.0, "3V3", "GND", spacing=5.0))
    fps.append(passive_tht("R1", 14.0, 13.5, "LED_DATA", "LED_A",
                           spacing=P.RES_THT_LEAD_SPACING))
    fps.append(passive_tht("C3", -13.0, 84.0, "3V3", "GND",
                           spacing=5.0))  # clear of U1

    for i, (x, y) in enumerate(P.PCB_HOLES, start=1):
        fps.append(mount_hole(f"H{i}", x, y))

    board.footprints = fps
    board.graphicItems = edge_cuts()
    board.zones = [gnd_zone("F.Cu"), gnd_zone("B.Cu")]
    return board


if __name__ == "__main__":
    out = os.path.join(os.path.dirname(__file__), "companion_carrier.kicad_pcb")
    build().to_file(out)
    # Round-trip check: re-parse what we wrote.
    reparsed = Board.from_file(out)
    print(f"OK: {out}")
    print(f"  {len(reparsed.footprints)} footprints, "
          f"{len(reparsed.nets)} nets, {len(reparsed.zones)} zones, "
          f"{len(reparsed.graphicItems)} edge items")
