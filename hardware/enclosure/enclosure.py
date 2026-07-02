"""FDM-printable handheld enclosure — CadQuery source.

Two printed parts:
  * front shell — front face + full-depth perimeter walls, keycap openings,
    mic + LED holes, side slot for the latch slide, bottom USB-C opening,
    and four screw bosses that the PCB seats against.
  * back lid — flush inset panel with spacer bosses; four M2 self-tapping
    screws come in from the back, through the lid and PCB, into the
    front-shell bosses (lid -> spacer -> PCB -> boss stack-up).

All dimensions come from hardware/design_params.py. Coordinates:
X = board X (centreline 0), Y = PCB_L/2 - board_y (so +Y is the mic/top
end), Z = 0 at the PCB front face, +Z toward the user.

Print orientation: front shell face-down (clean front surface, walls and
bosses build upward, no supports needed except small bridges over the USB
and slide openings); lid flat, boss side up.

Run from repo root:  python3 hardware/enclosure/enclosure.py
Outputs STL + STEP into hardware/enclosure/output/.
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
import design_params as P  # noqa: E402

import cadquery as cq  # noqa: E402

# ---- derived Z stack (see module docstring) ------------------------------
Z_PCB_TOP = 0.0
Z_PCB_BOT = -P.PCB_T                                   # -1.6
Z_FRONT_IN = P.CHOC_H_ABOVE_PCB + P.FRONT_GAP          # 5.5
Z_FRONT_OUT = Z_FRONT_IN + P.WALL                      # 7.5
Z_LID_IN = Z_PCB_BOT - P.BACK_GAP                      # -4.8
Z_LID_OUT = Z_LID_IN - P.WALL                          # -6.8

CAV_W = P.PCB_W + 2 * P.SHELL_CLEAR                    # 45.2
CAV_L = P.PCB_L + 2 * P.SHELL_CLEAR                    # 105.2
OUT_W = P.SHELL_W                                      # 49.2
OUT_L = P.SHELL_L                                      # 109.2
POCKET_W = OUT_W - 2.0                                 # lid pocket, 1 mm skirt
POCKET_L = OUT_L - 2.0
LID_CLEAR = 0.25
LID_W = POCKET_W - 2 * LID_CLEAR
LID_L = POCKET_L - 2 * LID_CLEAR


def ycad(y_board):
    return P.PCB_L / 2 - y_board


def rbox(w, l, z0, z1, r):
    """Rounded-corner rectangular prism between z0..z1."""
    return (cq.Workplane("XY", origin=(0, 0, z0))
            .rect(w, l).extrude(z1 - z0)
            .edges("|Z").fillet(r))


def _front_body():
    """Front shell without the cosmetic perimeter fillet."""
    shell = rbox(OUT_W, OUT_L, Z_LID_OUT, Z_FRONT_OUT, P.SHELL_CORNER_R)
    # main cavity (stops at the lid ledge) + lid pocket
    shell = shell.cut(rbox(CAV_W, CAV_L, Z_LID_IN, Z_FRONT_IN,
                           P.SHELL_CORNER_R - P.WALL))
    shell = shell.cut(rbox(POCKET_W, POCKET_L, Z_LID_OUT - 0.1, Z_LID_IN,
                           P.SHELL_CORNER_R - 1.0))

    # keycap openings through the front wall. At standard Choc pitch
    # (18 x 17 mm) adjacent caps sit only 0.5 mm apart, so per-key openings
    # would leave sub-millimetre FDM walls between them — the 2x2 cluster
    # gets one shared opening instead (macropad-style); PTT keeps its own.
    cluster = [(x, yb) for k, (x, yb) in P.KEY_POS.items() if k != "ptt"]
    cxs = [c[0] for c in cluster]
    cys = [c[1] for c in cluster]
    cl_w = (max(cxs) - min(cxs)) + P.CAP_W + 2 * P.CAP_HOLE_CLEAR
    cl_l = (max(cys) - min(cys)) + P.CAP_D + 2 * P.CAP_HOLE_CLEAR
    cl_c = (sum(cxs) / len(cxs), sum(cys) / len(cys))
    hole = rbox(cl_w, cl_l, Z_FRONT_IN - 0.1, Z_FRONT_OUT + 0.1, 1.5)
    shell = shell.cut(hole.translate((cl_c[0], ycad(cl_c[1]), 0)))
    px, pyb = P.KEY_POS["ptt"]
    hole = rbox(P.CAP_W + 2 * P.CAP_HOLE_CLEAR,
                P.CAP_D + 2 * P.CAP_HOLE_CLEAR,
                Z_FRONT_IN - 0.1, Z_FRONT_OUT + 0.1, 1.5)
    shell = shell.cut(hole.translate((px, ycad(pyb), 0)))

    # mic acoustic hole + LED window in the front wall
    for (x, yb), d in ((P.MIC_POS, P.MIC_SHELL_HOLE),
                       (P.LED_POS, P.LED_WINDOW)):
        shell = shell.cut(
            cq.Workplane("XY", origin=(x, ycad(yb), Z_FRONT_IN - 0.1))
            .circle(d / 2).extrude(P.WALL + 0.2))

    # right-wall slot for the latch slide knob
    knob_zc = P.SLIDE_BODY_H / 2
    slot = (cq.Workplane("YZ", origin=(CAV_W / 2 - 0.1, ycad(P.SLIDE_POS_Y),
                                       knob_zc))
            .rect(P.SLIDE_SLOT_L, P.SLIDE_SLOT_W)
            .extrude(P.WALL + P.SHELL_CLEAR + 0.2))
    shell = shell.cut(slot)

    # bottom-wall USB-C opening (XIAO's own connector at the PCB bottom edge)
    usb_zc = P.XIAO_PCB_T + P.XIAO_USB_H / 2
    usb = (cq.Workplane("XZ", origin=(0, -(CAV_L / 2 - 0.1), usb_zc))
           .rect(P.USB_CUT_W, P.USB_CUT_H)
           .extrude(P.WALL + P.SHELL_CLEAR + 0.2))
    shell = shell.cut(usb)

    # screw bosses: PCB seats against these (z 0 .. inner front face)
    for x, yb in P.PCB_HOLES:
        boss = (cq.Workplane("XY", origin=(x, ycad(yb), Z_PCB_TOP))
                .circle(P.BOSS_D / 2).extrude(Z_FRONT_IN - Z_PCB_TOP))
        shell = shell.union(boss)
        pilot = (cq.Workplane("XY", origin=(x, ycad(yb), Z_PCB_TOP - 0.1))
                 .circle(P.BOSS_PILOT / 2).extrude(4.6))
        shell = shell.cut(pilot)
    return shell


def build_front_shell():
    return _front_fillet(_front_body())


def _front_fillet(shell):
    """Break the sharp front-face edges (outer rim + opening rims) for hand
    feel; cosmetic only, so fall back to a chamfer or skip if OCC refuses."""
    for op, size in (("fillet", 0.8), ("chamfer", 0.5)):
        try:
            edges = shell.faces(">Z").edges()
            return getattr(edges, op)(size)
        except Exception as e:  # noqa: BLE001 - cosmetic feature only
            print(f"  note: front-face {op} {size} skipped ({e})")
    return shell


def build_back_lid():
    lid = rbox(LID_W, LID_L, Z_LID_OUT, Z_LID_IN,
               P.SHELL_CORNER_R - 1.0 - LID_CLEAR)
    for x, yb in P.PCB_HOLES:
        # spacer boss: lid inner face up to the PCB back face
        boss = (cq.Workplane("XY", origin=(x, ycad(yb), Z_LID_IN))
                .circle(P.BOSS_D / 2).extrude(-Z_LID_IN + Z_PCB_BOT))
        lid = lid.union(boss)
        # through hole + shallow counterbore for the screw head
        lid = lid.cut(
            cq.Workplane("XY", origin=(x, ycad(yb), Z_LID_OUT - 0.1))
            .circle(2.3 / 2).extrude(P.WALL + P.BACK_GAP + 0.2))
        lid = lid.cut(
            cq.Workplane("XY", origin=(x, ycad(yb), Z_LID_OUT - 0.1))
            .circle(4.4 / 2).extrude(1.0))
    return lid


if __name__ == "__main__":
    out = os.path.join(os.path.dirname(__file__), "output")
    os.makedirs(out, exist_ok=True)
    front = build_front_shell()
    lid = build_back_lid()
    cq.exporters.export(front, os.path.join(out, "front_shell.stl"))
    cq.exporters.export(front, os.path.join(out, "front_shell.step"))
    cq.exporters.export(lid, os.path.join(out, "back_lid.stl"))
    cq.exporters.export(lid, os.path.join(out, "back_lid.step"))
    bb = front.val().BoundingBox()
    print(f"front shell: {bb.xlen:.1f} x {bb.ylen:.1f} x {bb.zlen:.1f} mm")
    bb = lid.val().BoundingBox()
    print(f"back lid:    {bb.xlen:.1f} x {bb.ylen:.1f} x {bb.zlen:.1f} mm")
    print(f"outputs in {out}")
