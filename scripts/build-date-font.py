#!/usr/bin/env python3
"""Build a compact English timestamp font. Requires fonttools[woff], uharfbuzz."""
import argparse
import base64
import io
import re
from pathlib import Path

import uharfbuzz as hb
from fontTools.feaLib.builder import addOpenTypeFeaturesFromString
from fontTools.pens.ttGlyphPen import TTGlyphPen
from fontTools.ttLib import TTFont

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('semibold', type=Path, help='Static Inter Semibold font')
args = parser.parse_args()
repo = Path(__file__).resolve().parent.parent
font = TTFont(args.semibold)
cmap = font.getBestCmap()
for table in ['GSUB', 'GPOS', 'GDEF', 'DSIG']:
    if table in font:
        del font[table]

replacements = {
    'Yesterday': 'Yest', 'Monday': 'Mon', 'Tuesday': 'Tue',
    'Wednesday': 'Wed', 'Thursday': 'Thu', 'Friday': 'Fri',
    'Saturday': 'Sat', 'Sunday': 'Sun',
}
for space in [' ', '\u00a0', '\u202f', '']:
    replacements[space + 'AM'] = 'am'
    replacements[space + 'PM'] = 'pm'

rules = []
expected_glyphs = {}
for index, (source, replacement) in enumerate(replacements.items()):
    # Unsupported narrow spaces can use the ordinary space glyph in the cmap.
    for character in source:
        if ord(character) not in cmap:
            for table in font['cmap'].tables:
                if table.isUnicode():
                    table.cmap[ord(character)] = cmap[32]
            cmap[ord(character)] = cmap[32]
    glyph_name = f'compactdate{index}'
    pen = TTGlyphPen(font.getGlyphSet())
    advance = 0
    for character in replacement:
        glyph = cmap[ord(character)]
        pen.addComponent(glyph, (1, 0, 0, 1, advance, 0))
        advance += font['hmtx'][glyph][0]
    font['glyf'][glyph_name] = pen.glyph()
    font['hmtx'][glyph_name] = (advance, font['hmtx'][cmap[ord(replacement[0])]][1])
    source_glyphs = tuple(cmap[ord(c)] for c in source)
    # Space aliases may map to the same glyph: one substitution is sufficient.
    if source_glyphs not in expected_glyphs:
        rules.append('sub ' + ' '.join(source_glyphs) + f' by {glyph_name};')
        expected_glyphs[source_glyphs] = glyph_name

features = 'languagesystem DFLT dflt;\nlanguagesystem latn dflt;\nfeature liga {\n'
features += '\n'.join(rules) + '\n} liga;\n'
addOpenTypeFeaturesFromString(font, features)
for name_id, value in {
    1: 'Beeper Compact Dates', 2: 'Regular', 3: 'BeeperCompactDates-v1',
    4: 'Beeper Compact Dates', 6: 'BeeperCompactDates',
    16: 'Beeper Compact Dates', 17: 'Regular',
}.items():
    font['name'].setName(value, name_id, 3, 1, 0x409)

font.flavor = None
buffer = io.BytesIO()
font.save(buffer)
shaper = hb.Font(hb.Face(buffer.getvalue()))
order = font.getGlyphOrder()
def shape(text):
    buf = hb.Buffer()
    buf.add_str(text)
    buf.guess_segment_properties()
    hb.shape(shaper, buf, {'liga': True})
    return [order[g.codepoint] for g in buf.glyph_infos]

for source in replacements:
    assert shape(source) == [expected_glyphs[tuple(cmap[ord(c)] for c in source)]], source
for sample in ['12:20 AM', '12:01 PM', '9:05\u202fAM', '11:59\u00a0PM']:
    prefix = re.match(r'[0-9:]+', sample)[0]
    assert shape(sample)[:-1] == [cmap[ord(c)] for c in prefix], sample
    assert len(shape(sample)) == len(prefix) + 1, sample
for sample in ['10/22/2026', '12:20', 'Today', 'Nov 13']:
    assert shape(sample) == [cmap[ord(c)] for c in sample], sample

font.flavor = 'woff2'
buffer = io.BytesIO()
font.save(buffer)
start = '/* Compact timestamp font: abbreviate labels without rewriting dates. */'
end = '/* End compact timestamp font. */'
css = repo.joinpath('custom.css').read_text()
if start in css:
    before, rest = css.split(start, 1)
    _, after = rest.split(end, 1)
    css = before.rstrip() + after
license_text = repo.joinpath('INTER-LICENSE.txt').read_text()
block = start + '\n/* Derived from Inter Semibold. Renamed Beeper Compact Dates.\n'
block += license_text + '\n*/\n@font-face {\n'
block += '  font-family: "Beeper Compact Dates";\n  font-weight: 600;\n'
block += '  src: url("data:font/woff2;base64,' + base64.b64encode(buffer.getvalue()).decode() + '") format("woff2");\n}\n'
block += '''body .sidebar-thread .ThreadListItem-module__timestamp {
  font-family: "Beeper Compact Dates", var(--font-family) !important;
  font-weight: 600 !important;
  font-feature-settings: "liga" 1 !important;
  letter-spacing: 0 !important;
}
'''
block += end + '\n\n'
anchor = '/* Contextual font keeps the composer placeholder intact and bolds its chat name. */'
assert anchor in css
css = css.replace(anchor, block + anchor, 1)
repo.joinpath('custom.css').write_text(css)
print('Verified weekdays, yesterday, AM/PM spacing, and unchanged numeric dates.')
