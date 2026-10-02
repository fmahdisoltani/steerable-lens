from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageSequence
import re
root=Path(__file__).resolve().parents[1]
font=ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial Bold.ttf',20)
small=ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial.ttf',14)
for p in (root/'figures').glob('legacy_cat*.gif'):
 m=re.fullmatch(r'legacy_cat[123]_(.+)_amp(\d+)',p.stem);assert m
 title='Cat → '+m[1].replace('_',' ');subtitle='Live trajectory · amp '+m[2]
 def clean(im):
  im=im.convert('RGB');d=ImageDraw.Draw(im);d.rectangle((0,0,im.width,60),fill='white');d.text((16,11),title,font=font,fill='#222222');d.text((16,39),subtitle,font=small,fill='#555555');return im
 im=Image.open(p);durations=[];frames=[]
 for f in ImageSequence.Iterator(im): durations.append(f.info.get('duration',450));frames.append(clean(f))
 assert len(frames)==12
 frames[0].save(p,save_all=True,append_images=frames[1:],duration=durations,loop=0,disposal=2)
 poster=p.with_name(p.stem+'_poster.png');clean(Image.open(poster)).save(poster)
for p in [root/'index.html',root/'imagenet.html',root/'explore.html',root/'figures/animation_manifest.json']:
 s=p.read_text();s=re.sub(r'\bLegacy live','Live',s);s=re.sub(r'\blegacy O checkpoint','earlier O checkpoint',s)
 if p.suffix=='.html':
  s=re.sub(r'(figures/legacy_cat[^"?]+\.(?:gif|png))(?:\?v=\d+)?"',r'\1?v=3"',s)
 p.write_text(s)
