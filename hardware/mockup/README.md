# 3D mockup — integrated design, real component dimensions

Dimensionally representative assembly of the whole device: carrier PCB,
XIAO RP2040 module (header-mounted on the back, USB-C facing away into
the back shell), 5× Kailh Choc V1 switches + MBK-profile caps, PCM12SMTR
latch slide (knob through the right wall), an I2S mic breakout module
(front side), a plain THT LED, and both shell halves. Every envelope comes
from `../design_params.py` — the same values that drive the PCB and
enclosure, so the mockup can't silently disagree with them.

Render-color note: the PTT cap is shown orange purely so reviews can point
at it; the real build is all-blank caps per the minimalist decision.

## Files

- `mockup.py` — builds all parts, exports `output/mockup_assembly.step`
  (colored STEP; open in any CAD viewer) and `output/parts/*.stl`.
- `render.py` — shades the part meshes and writes `output/renders/*.png`:
  assembled front/rear iso, internals front/back, orthographic front view,
  exploded view.

```
python3 hardware/mockup/mockup.py && python3 hardware/mockup/render.py
```

Outputs are committed for review without tooling.
