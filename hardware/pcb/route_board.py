"""Route the carrier board headlessly: Specctra DSN out -> freerouting ->
SES back in -> GND stitching -> zone fill -> save.

This is step 2 of the board pipeline; run it after generate_pcb.py
whenever placement/netlist changes:

    1. python3 hardware/pcb/generate_pcb.py          (placement + netlist)
    2. <kicad-python> hardware/pcb/route_board.py <freerouting.jar>
    3. kicad-cli pcb drc ...                          (verify)
    4. kicad-cli pcb export gerbers/drill ...         (fab package)

<kicad-python> must be KiCad's own bundled python3 (it has the pcbnew
module); the plain system python3 does not. Example:

    ~/Applications/KiCad/KiCad.app/Contents/Frameworks/Python.framework/\
Versions/3.9/bin/python3 hardware/pcb/route_board.py \
        /path/to/freerouting.jar

Freerouting: https://github.com/freerouting/freerouting (jar release),
needs Java 21+ on PATH or at JAVA env var.

(SW5's GND pad gets a solid zone connection in generate_pcb.py rather
than a stitch track here -- the PTT switch's stem/post holes crowd the
F.Cu zone too much for 2 thermal spokes, and a stitch track only reached
an isolated island. Solid connect solves it at the source.)
"""

import os
import subprocess
import sys
import tempfile

import pcbnew

HERE = os.path.dirname(os.path.abspath(__file__))
BOARD_PATH = os.path.join(HERE, "companion_carrier.kicad_pcb")


def main():
    if len(sys.argv) < 2:
        sys.exit("usage: route_board.py /path/to/freerouting.jar")
    jar = sys.argv[1]
    java = os.environ.get("JAVA", "java")

    board = pcbnew.LoadBoard(BOARD_PATH)
    with tempfile.TemporaryDirectory() as td:
        dsn = os.path.join(td, "carrier.dsn")
        ses = os.path.join(td, "carrier.ses")
        if not pcbnew.ExportSpecctraDSN(board, dsn):
            sys.exit("DSN export failed")
        subprocess.run([java, "-jar", jar, "-de", dsn, "-do", ses,
                        "-mp", "50", "-da"], check=True)
        if not pcbnew.ImportSpecctraSES(board, ses):
            sys.exit("SES import failed")

    pcbnew.ZONE_FILLER(board).Fill(board.Zones())
    pcbnew.SaveBoard(BOARD_PATH, board)
    print(f"routed + filled: {BOARD_PATH}")
    print(f"  tracks: {len(board.GetTracks())}")


if __name__ == "__main__":
    main()
