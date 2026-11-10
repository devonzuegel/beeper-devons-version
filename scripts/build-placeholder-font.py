#!/usr/bin/env python3
"""Requires fonttools[woff] and uharfbuzz. Uses matching static Inter fonts."""
from pathlib import Path
import struct,json,copy,io,base64
from fontTools.ttLib import TTFont
from fontTools.feaLib.builder import addOpenTypeFeaturesFromString
import uharfbuzz as hb
import argparse
parser = argparse.ArgumentParser(description="Embed a contextual Inter-derived placeholder font in custom.css.")
parser.add_argument("medium", type=Path, help="Inter Medium font file")
parser.add_argument("bold", type=Path, help="Matching Inter Bold font file")
args = parser.parse_args()
repo = Path(__file__).resolve().parent.parent
regular, bold = TTFont(args.medium), TTFont(args.bold)
order=list(regular.getGlyphOrder()); rename={g:g+'.namebold' for g in bold.getGlyphOrder()}
for g in bold.getGlyphOrder():
 clone=copy.deepcopy(bold['glyf'][g])
 if clone.isComposite():
  for component in clone.components: component.glyphName=rename[component.glyphName]
 regular['glyf'][rename[g]]=clone
 regular['hmtx'][rename[g]]=bold['hmtx'][g]
regular.setGlyphOrder(order+list(rename.values()))
for table in ['GSUB','GPOS','GDEF','DSIG']:
 if table in regular: del regular[table]
cmap=regular.getBestCmap(); normal=sorted(set(cmap.values()) & set(rename)); heavy=[rename[g] for g in normal]
def glyphs(text): return ' '.join(cmap[ord(c)] for c in text)
fea='languagesystem DFLT dflt;\nlanguagesystem latn dflt;\n'
fea+='@regular = ['+' '.join(normal)+'];\n@namebold = ['+' '.join(heavy)+'];\n'
fea+='feature calt { lookup NameWeight {\n'
for network in ['iMessage','Signal','WhatsApp','Telegram','Facebook Messenger','Beeper','X','Twitter']:
 fea+='ignore sub @namebold '+cmap[32]+"' "+glyphs('on '+network)+';\n'
fea+='sub '+glyphs('Message ')+" @regular' by @namebold;\n"
fea+="sub @namebold @regular' by @namebold;\n} NameWeight; } calt;\n"
addOpenTypeFeaturesFromString(regular,fea)
for id,value in [(1,'Beeper Placeholder'),(2,'Regular'),(4,'Beeper Placeholder Regular'),(6,'BeeperPlaceholder-Regular'),(3,'BeeperPlaceholder-v1'),(16,'Beeper Placeholder'),(17,'Regular')]:
 regular['name'].setName(value,id,3,1,0x409)
regular.flavor=None; buffer=io.BytesIO(); regular.save(buffer)
face=hb.Face(buffer.getvalue()); font=hb.Font(face)
for text in ['Message Alex Rivera on iMessage','Message Alex & Sam on Signal','Message Zoë García on WhatsApp']:
 buf=hb.Buffer();buf.add_str(text);buf.guess_segment_properties();hb.shape(font,buf,{'calt':True})
 results=[regular.getGlyphOrder()[g.codepoint] for g in buf.glyph_infos]
 expected = ['.' if i < len('Message ') or i >= text.rindex(' on ') else 'B' for i in range(len(text))]
 actual = ['B' if x.endswith('.namebold') else '.' for x in results]
 assert actual == expected, (text, actual, expected)
regular.flavor='woff2';output=io.BytesIO();regular.save(output)
marker = '/* Contextual font keeps the composer placeholder intact and bolds its chat name. */'
css = repo.joinpath('custom.css').read_text().split(marker)[0].rstrip() + '\n'
license_text = repo.joinpath('INTER-LICENSE.txt').read_text()
css+='\n'+marker+'\n/* Derived from Inter Medium / Bold. Renamed Beeper Placeholder.\n'+license_text+'\n*/\n@font-face {\n font-family: "Beeper Placeholder";\n font-weight: 500;\n src: url("data:font/woff2;base64,'+base64.b64encode(output.getvalue()).decode()+'") format("woff2");\n}\n.ComposeMessage-module__textArea p.is-editor-empty:only-child[data-placeholder^="Message "]::before {\n font-family: "Beeper Placeholder", var(--font-family) !important;\n font-weight: 500 !important;\n font-feature-settings: "calt" 1 !important;\n}\n'
repo.joinpath('custom.css').write_text(css)
print('woff2 bytes',len(output.getvalue()))
