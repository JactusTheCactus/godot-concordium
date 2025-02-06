from fontTools.ttLib import TTFont
from fontTools.pens.basePen import BasePen
from fontTools.pens.ttGlyphPen import TTGlyphPen
from fontTools.fontBuilder import FontBuilder
from PIL import Image
import os

# Path to folder containing glyph images
GLYPH_FOLDER = "glyphs"
FONT_NAME = "AbugidaFont"
OUTPUT_TTF = f"{FONT_NAME}.ttf"
fileAddress = "D:/Downoads/ProgrammingProjects/godotProjects/concordium/assets/fonts/Abugida"

# Define glyph mappings (Unicode: Filename)
GLYPH_MAP = {
    "space": 0x0020,
    "period": 0x002E,
    "comma": 0x002C,
    "question": 0x003F,
    "a": 0x0061,
    "á": 0x00E1,
    "e": 0x0065,
    "é": 0x00E9,
    "i": 0x0069,
    "o": 0x006F,
    "ó": 0x00F3,
    "u": 0x0075,
    "ú": 0x00FA,
    "b": 0x0062,
    "c": 0x0063,
    "d": 0x0064,
    "ð": 0x00F0,
    "f": 0x0066,
    "g": 0x0067,
    "h": 0x0068,
    "j": 0x006A,
    "k": 0x006B,
    "l": 0x006C,
    "m": 0x006D,
    "n": 0x006E,
    "ŋ": 0x014B,
    "p": 0x0070,
    "r": 0x0072,
    "s": 0x0073,
    "ś": 0x015B,
    "t": 0x0074,
    "þ": 0x00FE,
    "v": 0x0076,
    "w": 0x0077,
    "x": 0x0078,
    "y": 0x0079,
    "z": 0x007A,
    "ź": 0x017A
}

# Initialize font builder
fb = FontBuilder(1000, isTTF=True)
glyph_order = [".notdef"] + list(GLYPH_MAP.keys())
fb.setupGlyphOrder(glyph_order)

# Ensure .notdef glyph exists
glyphs = {}
pen = TTGlyphPen(None)
pen.moveTo((0, 0))
pen.lineTo((100, 0))
pen.lineTo((100, 100))
pen.lineTo((0, 100))
pen.closePath()
glyphs[".notdef"] = pen.glyph()
fb.setupCharacterMap({codepoint: name for name, codepoint in GLYPH_MAP.items()})

# Process each glyph image and create its corresponding glyph
for filename, unicode_val in GLYPH_MAP.items():
    image_path = f"{fileAddress}/sprites/{GLYPH_FOLDER}/{filename}.png"

    if not os.path.exists(image_path):
        print(f"Warning: Missing {image_path}")
        continue

    # Load image and convert to monochrome
    img = Image.open(image_path).convert("L").transpose(Image.FLIP_TOP_BOTTOM)
    width, height = img.size

    # Convert image to font glyph
    pen = TTGlyphPen(None)
    for x in range(width):
        for y in range(height):
            if img.getpixel((x, y)) < 128:  # Threshold for black pixels
                pen.moveTo((x, y))
                pen.lineTo((x + 1, y))
                pen.lineTo((x + 1, y + 1))
                pen.lineTo((x, y + 1))
                pen.closePath()
    glyphs[filename] = pen.glyph()

# Setup font properties
fb.setupGlyf(glyphs)
fb.setupHorizontalMetrics({name: (600, 0) for name in glyph_order})
fb.setupHorizontalHeader(ascent=800, descent=200)
fb.setupOS2()
fb.setupMaxp()  # <- Ensures max values for font

# Function to sanitize string and use UTF-8 encoding
def sanitize_string(s):
    # Ensure that the string is encoded using UTF-8, which supports 'ŋ' (U+014B)
    return s.encode('utf-8').decode('utf-8')

# Setup name table with UTF-8 encoding (use the custom font name)
fb.setupNameTable(
    {
        1: sanitize_string(FONT_NAME),  # Name for the font (handles 'ŋ')
        2: "Regular",                   # Style
        3: "1.0",                       # Version
        4: sanitize_string(f"{FONT_NAME} Regular"),  # Full name
        5: "Version 1.0",               # Description
        6: FONT_NAME.replace(" ", ""),  # Postscript name
    }
)

# Setup cmap table to map Unicode values to glyphs
cmap = {
    unicode_val: filename for filename, unicode_val in GLYPH_MAP.items()
}
fb.setupCharacterMap(cmap)

# Bypass post table creation if issues persist (workaround)
font = fb.font

# Save the font to the specified path
try:
    font.save(f"{fileAddress}/{OUTPUT_TTF}")
    print(f"Font saved as {OUTPUT_TTF}")
except Exception as e:
    print(f"Error saving font: {e}")
