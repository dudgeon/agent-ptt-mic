"""Render review PNGs of the mockup (no CAD tool needed to look at them).

Reads the per-part STLs written by mockup.py, shades them with a simple
directional-light model, and writes several views into output/renders/.

Run from repo root, after mockup.py:  python3 hardware/mockup/render.py
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
from mockup import build_all, PARTS  # noqa: E402  (for the color table)

PARTS_DIR = os.path.join(HERE, "output", "parts")
RENDER_DIR = os.path.join(HERE, "output", "renders")

LIGHT = np.array([0.35, -0.5, 0.8])
LIGHT = LIGHT / np.linalg.norm(LIGHT)


def load_part(name, max_edge=4.0):
    mesh = trimesh.load(os.path.join(PARTS_DIR, f"{name}.stl"))
    # subdivide so matplotlib's per-polygon depth sort has less to get wrong
    v, f = trimesh.remesh.subdivide_to_size(mesh.vertices, mesh.faces,
                                            max_edge=max_edge)
    return trimesh.Trimesh(vertices=v, faces=f, process=False)


def shade(color, normals):
    lam = np.clip(normals @ LIGHT, 0, 1)
    rgb = np.array(color)[None, :] * (0.5 + 0.5 * lam[:, None])
    return np.clip(rgb, 0, 1)


def render(parts, fname, elev=28, azim=-55, ortho=False, title=""):
    """parts: list of (mesh, color, alpha, z_offset)."""
    tris, cols = [], []
    for mesh, color, alpha, dz in parts:
        m = mesh.copy()
        m.apply_translation((0, 0, dz))
        n = m.face_normals
        c = shade(color, n)
        c = np.concatenate([c, np.full((len(c), 1), alpha)], axis=1)
        tris.append(m.triangles)
        cols.append(c)
    tri = np.concatenate(tris)
    col = np.concatenate(cols)

    fig = plt.figure(figsize=(9, 9), dpi=130)
    ax = fig.add_subplot(111, projection="3d")
    coll = Poly3DCollection(tri, facecolors=col, edgecolors="none")
    ax.add_collection3d(coll)

    lo, hi = tri.reshape(-1, 3).min(0), tri.reshape(-1, 3).max(0)
    mid, span = (lo + hi) / 2, (hi - lo).max() * 0.62
    ax.set_xlim(mid[0] - span, mid[0] + span)
    ax.set_ylim(mid[1] - span, mid[1] + span)
    ax.set_zlim(mid[2] - span, mid[2] + span)
    ax.view_init(elev=elev, azim=azim)
    if ortho:
        ax.set_proj_type("ortho")
    ax.set_axis_off()
    ax.set_title(title, fontsize=11)
    fig.tight_layout()
    fig.savefig(os.path.join(RENDER_DIR, fname), bbox_inches="tight")
    plt.close(fig)
    print(f"  {fname}")


def main():
    os.makedirs(RENDER_DIR, exist_ok=True)
    build_all()  # just for the PARTS color table; solids not reused
    colors = {name: color for name, (_, color) in PARTS.items()}
    meshes = {name: load_part(name) for name in colors}

    internals = [n for n in colors if n not in ("front_shell", "back_lid")]

    def pl(names, alpha=1.0, dz=0.0, alpha_map=None, dz_map=None):
        return [(meshes[n], colors[n],
                 (alpha_map or {}).get(n, alpha),
                 (dz_map or {}).get(n, dz)) for n in names]

    print("rendering:")
    render(pl(list(colors)), "assembled_iso.png",
           title="Assembled — front iso (caps proud of the front face)")
    render(pl(list(colors)), "assembled_rear_iso.png", elev=-32, azim=125,
           title="Assembled — rear iso (lid, USB-C opening at bottom edge)")
    render(pl(internals), "internals_iso.png",
           title="Internals — carrier PCB as populated (no shells)")
    render(pl(internals), "internals_rear_iso.png", elev=-30, azim=115,
           title="Internals — back side (mic bottom-port, switch pins)")
    render(pl(list(colors)), "front_ortho.png", elev=90, azim=-90, ortho=True,
           title="Front view — 2x2 keys, PTT below, LED+mic top, latch right")
    render(pl(list(colors),
              dz_map={"front_shell": 34.0, "back_lid": -26.0}),
           "exploded_iso.png",
           title="Exploded — front shell / populated PCB / back lid")


if __name__ == "__main__":
    main()
