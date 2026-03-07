#!/usr/bin/env python3
"""Convert Instrument_Serif.glyphs to two UFOs (Regular + Black) and a designspace."""

import shutil
from pathlib import Path
from glyphsLib import GSFont, to_ufos
from fontTools.designspaceLib import (
    DesignSpaceDocument,
    AxisDescriptor,
    SourceDescriptor,
    InstanceDescriptor,
)
import ufoLib2

SOURCES_DIR = Path(__file__).parent

# Step 1: Convert .glyphs to UFO using glyphsLib
font = GSFont(str(SOURCES_DIR / "Instrument_Serif.glyphs"))
ufos = to_ufos(font)
ufo = ufos[0]  # Single master, so one UFO

# Step 2: Save as Regular UFO
regular_path = SOURCES_DIR / "InstrumentSerif-Regular.ufo"
black_path = SOURCES_DIR / "InstrumentSerif-Black.ufo"

# Remove existing if present
for p in [regular_path, black_path]:
    if p.exists():
        shutil.rmtree(p)

ufo.save(str(regular_path), overwrite=True)
print(f"Saved {regular_path}")

# Step 3: Copy to Black UFO
shutil.copytree(regular_path, black_path)
print(f"Copied to {black_path}")

# Step 4: Update font info for both UFOs
DESIGNER = "Eli Heuer"
VENDOR_ID = "FTG "

for ufo_path, style_name, weight_class in [
    (regular_path, "Regular", 400),
    (black_path, "Black", 900),
]:
    f = ufoLib2.Font.open(ufo_path)

    f.info.familyName = "Instrument Serif"
    f.info.styleName = style_name
    f.info.styleMapFamilyName = "Instrument Serif"
    f.info.styleMapStyleName = "regular" if style_name == "Regular" else "bold"

    f.info.openTypeNameDesigner = DESIGNER
    f.info.openTypeOS2WeightClass = weight_class
    f.info.openTypeOS2VendorID = VENDOR_ID

    # Use Typo Metrics
    f.info.openTypeOS2Selection = [7]  # bit 7 = USE_TYPO_METRICS

    f.info.openTypeNameManufacturer = DESIGNER
    f.info.openTypeNameDesignerURL = None
    f.info.openTypeNameManufacturerURL = None

    f.save(ufo_path, overwrite=True)
    print(f"Updated font info for {ufo_path}")

# Step 5: Create designspace
ds = DesignSpaceDocument()

# Weight axis
weight_axis = AxisDescriptor()
weight_axis.tag = "wght"
weight_axis.name = "Weight"
weight_axis.minimum = 400
weight_axis.default = 400
weight_axis.maximum = 900
weight_axis.map = None
ds.addAxis(weight_axis)

# Regular source (default)
regular_src = SourceDescriptor()
regular_src.filename = "InstrumentSerif-Regular.ufo"
regular_src.familyName = "Instrument Serif"
regular_src.styleName = "Regular"
regular_src.location = {"Weight": 400}
ds.addSource(regular_src)

# Black source
black_src = SourceDescriptor()
black_src.filename = "InstrumentSerif-Black.ufo"
black_src.familyName = "Instrument Serif"
black_src.styleName = "Black"
black_src.location = {"Weight": 900}
ds.addSource(black_src)

# Instances
for name, weight in [("Regular", 400), ("Black", 900)]:
    inst = InstanceDescriptor()
    inst.familyName = "Instrument Serif"
    inst.styleName = name
    inst.location = {"Weight": weight}
    ds.addInstance(inst)

ds_path = SOURCES_DIR / "InstrumentSerif.designspace"
ds.write(str(ds_path))
print(f"Saved {ds_path}")

print("\nDone!")
