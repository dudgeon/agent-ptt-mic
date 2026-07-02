"""Zoomed-in detail render of the mic + LED region, front side.

2026-07-02: the mic is now a breakout module (~18 x 12mm) on the front,
big enough to be visible in the regular full-board renders -- this script
is kept mainly for the LED close-up and as a quick visual check that both
parts sit where design_params.py says they should.

Run after mockup.py:  python3 hardware/mockup/render_mic_detail.py
"""
import os
import sys

import numpy as np
import trimesh
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from mpl_toolkits.mplot3d.art3d import Poly3DCollection  # noqa: E402

HERE = os.path.dirname(__file__)
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, ".."))
from mockup import build_all, PARTS, ycad  # noqa: E402
import design_params as P  # noqa: E402

PARTS_DIR = os.path.join(HERE, "output", "parts")
RENDER_DIR = os.path.join(HERE, "output", "renders")
LIGHT = np.array([0.35, -0.5, 0.8])
LIGHT = LIGHT / np.linalg.norm(LIGHT)


def load_part(name, max_edge=None):
    mesh = trimesh.load(os.path.join(PARTS_DIR, f"{name}.stl"))
    if max_edge is None:
        return mesh
    v, f = trimesh.remesh.subdivide_to_size(mesh.vertices, mesh.faces,
                                            max_edge=max_edge)
    return trimesh.Trimesh(vertices=v, faces=f, process=False)


def shade(color, normals):
    lam = np.clip(normals @ LIGHT, 0, 1)
    rgb = np.array(color)[None, :] * (0.5 + 0.5 * lam[:, None])
    return np.clip(rgb, 0, 1)


def render(names, meshes, colors, fname, center, half, elev, azim, title):
    tris, cols = [], []
    for n in names:
        m = meshes[n]
        c = shade(colors[n], m.face_normals)
        c = np.concatenate([c, np.full((len(c), 1), 1.0)], axis=1)
        tris.append(m.triangles)
        cols.append(c)
    tri = np.concatenate(tris)
    col = np.concatenate(cols)

    fig = plt.figure(figsize=(8, 8), dpi=150)
    ax = fig.add_subplot(111, projection="3d")
    ax.add_collection3d(Poly3DCollection(tri, facecolors=col,
                                         edgecolors="none"))
    ax.set_xlim(center[0] - half, center[0] + half)
    ax.set_ylim(center[1] - half, center[1] + half)
    ax.set_zlim(center[2] - half, center[2] + half)
    ax.view_init(elev=elev, azim=azim)
    ax.set_axis_off()
    ax.set_title(title, fontsize=10)
    fig.tight_layout()
    fig.savefig(os.path.join(RENDER_DIR, fname), bbox_inches="tight")
    plt.close(fig)
    print(f"  {fname}")


def main():
    build_all()
    colors = {name: color for name, (_, color) in PARTS.items()}
    names = ["pcb", "mic", "led", "xiao"]
    # Flat-shaded per-face -- subdivision buys nothing here and is
    # ruinously expensive on the full-size PCB mesh at a sub-mm edge
    # length. Skip it; box-like parts render fine at native tessellation.
    meshes = {n: load_part(n) for n in names}

    mic_x, mic_yb = P.MIC_POS
    mic_center = (mic_x, ycad(mic_yb), P.MIC_BRK_STANDOFF + P.MIC_BRK_H / 2)
    render(["pcb", "mic"], meshes, colors, "mic_detail_front.png",
           center=mic_center, half=14.0, elev=30, azim=-60,
           title=f"Mic detail (front side) — MK1 breakout module, "
                 f"~{P.MIC_BRK_L}x{P.MIC_BRK_W}mm, at board {P.MIC_POS}")

    led_x, led_yb = P.LED_POS
    led_center = (led_x, ycad(led_yb), P.LED_THT_H / 2)
    render(["pcb", "led"], meshes, colors, "led_detail_front.png",
           center=led_center, half=6.0, elev=30, azim=-60,
           title=f"LED detail (front side) — D1 3mm THT LED + R1, "
                 f"at board {P.LED_POS}")


if __name__ == "__main__":
    main()
