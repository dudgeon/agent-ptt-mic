"""Representative 3D mockup of the assembled device.

Every component is modelled at its real datasheet envelope (dimensions from
hardware/design_params.py — same source the PCB and enclosure use), placed
at its true PCB position: XIAO RP2040 module (header-mounted on the BACK,
with its USB-C connector), 5x Kailh Choc V1 switches with MBK-profile caps,
PCM12SMTR latch slide, an I2S mic breakout module (front side), a plain
THT status LED, carrier PCB, and both shell halves.

2026-07-02: XIAO/mic/LED all switched from the flush-SMD-mount revision to
header/THT mounting -- see design_params.py's module docstring for why.

Outputs into hardware/mockup/output/:
  * mockup_assembly.step   — full colored STEP assembly
  * parts/*.stl            — individual meshes (used by render.py)

Run from repo root:  python3 hardware/mockup/mockup.py
Then render PNGs:    python3 hardware/mockup/render.py
"""

import os
import sys

HERE = os.path.dirname(__file__)
sys.path.insert(0, os.path.join(HERE, ".."))
sys.path.insert(0, os.path.join(HERE, "..", "enclosure"))
import design_params as P  # noqa: E402
import enclosure as ENC  # noqa: E402

import cadquery as cq  # noqa: E402

ycad = ENC.ycad


def box_at(w, l, h, x, yb, z0, r=0.0):
    """Rect prism centred at board (x, yb), from z0 up h. Optional corner r."""
    wp = cq.Workplane("XY", origin=(x, ycad(yb), z0)).rect(w, l).extrude(h)
    if r > 0:
        wp = wp.edges("|Z").fillet(r)
    return wp


def cyl_at(d, h, x, yb, z0):
    """Cylinder centred at board (x, yb), from z0 up h."""
    return (cq.Workplane("XY", origin=(x, ycad(yb), z0))
            .circle(d / 2).extrude(h))


def build_pcb():
    pcb = (cq.Workplane("XY", origin=(0, 0, -P.PCB_T))
           .rect(P.PCB_W, P.PCB_L).extrude(P.PCB_T)
           .edges("|Z").fillet(P.PCB_CORNER_R))
    for x, yb in P.PCB_HOLES:
        pcb = pcb.cut(cq.Workplane("XY", origin=(x, ycad(yb), -P.PCB_T - 0.1))
                      .circle(P.PCB_HOLE_D / 2).extrude(P.PCB_T + 0.2))
    return pcb


def build_choc_switch(x, yb):
    body = box_at(P.CHOC_BODY_UNDER, P.CHOC_BODY_UNDER, 2.2, x, yb, 0)
    flange = box_at(P.CHOC_BODY, P.CHOC_BODY, P.CHOC_H_ABOVE_PCB - 2.2,
                    x, yb, 2.2)
    stem = box_at(11.0, 5.5, P.CAP_TOP_ABOVE_PCB - P.CAP_H
                  - P.CHOC_H_ABOVE_PCB, x, yb, P.CHOC_H_ABOVE_PCB)
    return body.union(flange).union(stem)


def build_keycap(x, yb):
    z0 = P.CAP_TOP_ABOVE_PCB - P.CAP_H
    return box_at(P.CAP_W, P.CAP_D, P.CAP_H, x, yb, z0, r=1.8)


def build_xiao():
    """Module hangs off the carrier's BACK on its own header pins: walk
    outward (more negative Z) from the carrier back face (-PCB_T) through
    the standoff gap, then the module's own PCB, arriving at its
    component/USB-C face (which points away from the carrier)."""
    yb = P.XIAO_POS_Y
    inner_z = -P.PCB_T - P.XIAO_MODULE_STANDOFF        # module PCB inner face
    outer_z = inner_z - P.XIAO_PCB_T                    # module PCB outer (component) face
    board = box_at(P.XIAO_W, P.XIAO_L, P.XIAO_PCB_T, 0, yb, outer_z, r=1.5)
    chip = box_at(4.0, 3.5, 0.9, 0, yb - 2.0, outer_z - 0.9)
    usb_yb = yb + P.XIAO_L / 2 + P.XIAO_USB_OVERHANG - 7.35 / 2
    usb = box_at(P.XIAO_USB_W, 7.35, P.XIAO_USB_H, 0, usb_yb,
                 outer_z - P.XIAO_USB_H, r=1.2)
    # header pins bridging the standoff gap (cosmetic, approximate)
    pins = cyl_at(1.0, P.XIAO_MODULE_STANDOFF, -P.XIAO_HDR_ROW_SPACING / 2,
                  yb - 3 * P.XIAO_PAD_PITCH, inner_z)
    pins = pins.union(cyl_at(1.0, P.XIAO_MODULE_STANDOFF,
                             P.XIAO_HDR_ROW_SPACING / 2,
                             yb - 3 * P.XIAO_PAD_PITCH, inner_z))
    return board.union(chip).union(usb).union(pins)


def build_slide():
    x_body = P.PCB_W / 2 - P.SLIDE_BODY_W / 2
    body = box_at(P.SLIDE_BODY_W, P.SLIDE_BODY_L, P.SLIDE_BODY_H,
                  x_body, P.SLIDE_POS_Y, 0)
    knob = (cq.Workplane("YZ",
                         origin=(P.PCB_W / 2 - 0.5, ycad(P.SLIDE_POS_Y),
                                 P.SLIDE_BODY_H / 2))
            .rect(P.SLIDE_KNOB, P.SLIDE_KNOB)
            .extrude(0.5 + P.SLIDE_KNOB_EXT))
    return body.union(knob)


def build_mic():
    """Mic BREAKOUT MODULE, front side, standing off the carrier on its
    own header pins (design_params.py MIC_BRK_STANDOFF) -- not a bare chip
    reflowed flush, per the pre-soldered-XIAO/header-everything revision."""
    x, yb = P.MIC_POS
    return box_at(P.MIC_BRK_L, P.MIC_BRK_W, P.MIC_BRK_H, x, yb,
                  P.MIC_BRK_STANDOFF, r=1.0)


def build_led():
    """Plain 3mm THT LED (dome) + its series resistor, front side."""
    x, yb = P.LED_POS
    led = cyl_at(P.LED_THT_DIA, P.LED_THT_H, x, yb, 0)
    res = box_at(P.RES_THT_LEN, P.RES_THT_DIA, P.RES_THT_DIA,
                 x, yb + 5.5, 0.5)
    return led.union(res)


PARTS = {}  # name -> (solid, color rgb 0-1)


def build_all():
    PARTS["pcb"] = (build_pcb(), (0.10, 0.45, 0.20))
    for name, (x, yb) in P.KEY_POS.items():
        PARTS[f"switch_{name}"] = (build_choc_switch(x, yb),
                                   (0.35, 0.35, 0.38))
        cap_color = (0.85, 0.45, 0.10) if name == "ptt" else (0.12, 0.12, 0.13)
        PARTS[f"cap_{name}"] = (build_keycap(x, yb), cap_color)
    PARTS["xiao"] = (build_xiao(), (0.15, 0.25, 0.55))
    PARTS["slide"] = (build_slide(), (0.75, 0.75, 0.78))
    PARTS["mic"] = (build_mic(), (0.80, 0.78, 0.72))
    PARTS["led"] = (build_led(), (0.95, 0.95, 0.90))
    PARTS["front_shell"] = (ENC.build_front_shell(), (0.82, 0.82, 0.84))
    PARTS["back_lid"] = (ENC.build_back_lid(), (0.60, 0.60, 0.63))
    return PARTS


if __name__ == "__main__":
    out = os.path.join(HERE, "output")
    parts_dir = os.path.join(out, "parts")
    os.makedirs(parts_dir, exist_ok=True)
    build_all()

    asm = cq.Assembly(name="companion_peripheral")
    for name, (solid, color) in PARTS.items():
        asm.add(solid, name=name, color=cq.Color(*color))
        cq.exporters.export(solid, os.path.join(parts_dir, f"{name}.stl"))
    asm.save(os.path.join(out, "mockup_assembly.step"))
    print(f"OK: {len(PARTS)} parts -> {out}")
