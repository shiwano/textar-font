#!/usr/bin/env fontforge -script

import pickle

import fontforge
import psMat


IPA_FONT = "ipagp.ttf"
PATCH_FONT = "textar-patch.otf"
MSPG_GLYPH_DATA = "mspg_glyph_data.pickle"
OUTPUT_FILE = "textar.sfd"


def scale(glyph, scalex, scaley):
    glyph.transform(psMat.scale(scalex, scaley))

def move(glyph, x, y):
    glyph.transform(psMat.translate(x, y))

def copy_from_patch_font(font, patch_font, encodings):    
    font.selection.none()
    patch_font.selection.none()
    
    for encoding in encodings:
        font.selection.select(("more", None), encoding)
        patch_font.selection.select(("more", None), encoding)
        
    patch_font.copy()
    font.paste()
    font.selection.none()
    patch_font.selection.none()

font = fontforge.open(IPA_FONT)
f = open(MSPG_GLYPH_DATA, "rb")
mspg_glyph_data = pickle.load(f)
f.close()
font.selection.all()

for glyph in font.selection.byGlyphs:
    d = mspg_glyph_data.get(glyph.encoding)
    
    if d and glyph.isWorthOutputting():
        mspg_width = d["width"]
        mspg_bbox = d["bbox"]
        mspg_lbear = d["lbearing"]
        width = glyph.width
        bbox = glyph.boundingBox()
        mspg_disty = 0
        mspg_boxw = mspg_bbox[2] - mspg_bbox[0]
        mspg_boxh = mspg_bbox[3] - mspg_bbox[1]
        boxw = bbox[2] - bbox[0]
        boxh = bbox[3] - bbox[1]
        
        if boxw:
            scalex = mspg_boxw / boxw
        else:
            scalex = 1
        
        if boxw < boxh and scalex > 1.1:
            scalex = 1.1
            mspg_lbear = mspg_lbear + (mspg_boxw - (boxw * scalex)) / 2
            mspg_lbear = round(mspg_lbear)

        if boxh:
            scaley = mspg_boxh / boxh
        else:
            scaley = 1
        
        if boxh < boxw and scaley > 1.1:
            scaley = 1.1
            mspg_disty = mspg_disty + (mspg_boxh - (boxh * scaley)) / 2
       
        if 0.98 > scalex or scalex > 1.02 or 0.98 > scaley or scaley > 1.02:
            scale(glyph, scalex, scaley)
        
        y = mspg_disty + mspg_bbox[1] - glyph.boundingBox()[1]
        move(glyph, 0, y)
        glyph.left_side_bearing = mspg_lbear
        glyph.width = mspg_width
            
font.selection.all()
font.em = 1000
patch_font = fontforge.open(PATCH_FONT)
encodings = [65392, 12540, 124, 8214, 65295, 65340, 8208, 8213, 65343, 95,
             65507, 175, 8722, 34, 39, 65282, 33, 106, 9679, 9678, 9675,
             12295, 8721, 60, 62, 65396, 65386, 8194, 8195, 8201]
copy_from_patch_font(font, patch_font, encodings)
font.save(OUTPUT_FILE)
print "Saved a SFD file. Run the 'textar.pe' script."
