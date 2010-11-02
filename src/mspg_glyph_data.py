#!/usr/bin/env fontforge -script

import pickle
import fontforge


MSPG_FONT = "MSPgothic.ttf"
OUTPUT_FILE = "mspg_glyph_data.pickle"


font = fontforge.open(MSPG_FONT)
font.selection.all()
font.em = 2048
ascent_scale = 1802.0 / font.ascent
descent_scale = 246.0 / (font.em - font.ascent)
glyph_data = {}

for glyph in font.selection.byGlyphs:
    if glyph.isWorthOutputting():
        xmin, ymin, xmax, ymax = glyph.boundingBox()
        
        if ymin > 0:
            ymin *= ascent_scale
        else:
            ymin *= descent_scale
        
        if ymax > 0:
            ymax *= ascent_scale
        else:
            ymax *= descent_scale
        
        d = {"width": glyph.width,
             "bbox": (xmin, ymin, xmax, ymax),
             "lbearing": glyph.left_side_bearing}
        glyph_data[glyph.encoding] = d

f = open(OUTPUT_FILE, "wb")
pickle.dump(glyph_data, f)
f.close()
print "Created " + OUTPUT_FILE + "."
