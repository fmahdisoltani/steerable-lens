"""Build faithful twelve-stage animations from the supplied close-up strips."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import hashlib, json, shutil, sys
root=Path(__file__).resolve().parents[1]
cases=[('cat_closeup','Cat · close-up trajectory',None),('dog1_face_amp120','Dog · close-up 1',120),('dog1_face_amp1000','Dog · close-up 1',1000),('dog2_face_amp1000','Dog · close-up 2',1000),('dog3_face_amp120','Dog · close-up 3',120),('dog3_face_amp1000','Dog · close-up 3',1000)]
font=ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial.ttf',16)
small=ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial.ttf',13)
entries=[]
for idx,(name,title,amp) in enumerate(cases):
 dest=root/'figures'/f'{name}_strip.png'
 if len(sys.argv)>1:
  src=Path(sys.argv[1]) if idx==0 else Path(sys.argv[2])/f'{name}.png'
  shutil.copyfile(src,dest)
 im=Image.open(dest).convert('RGB');assert im.size==(2688,300),im.size
 frames=[]
 for i in range(12):
  frame=Image.new('RGB',(500,402),'white');d=ImageDraw.Draw(frame)
  d.text((16,12),title,font=font,fill='#222222')
  subtitle=f'Amplification {amp} · 12 recorded stages' if amp else '12 recorded stages'
  d.text((16,38),subtitle,font=small,fill='#555555')
  d.text((75,68),'Source (fixed)',font=small,fill='#222222')
  d.text((315,68),f'Stage {i+1} of 12',font=small,fill='#222222')
  frame.paste(im.crop((0,76,224,300)),(16,90))
  frame.paste(im.crop((i*224,76,(i+1)*224,300)),(260,90))
  frame.paste(im.crop((i*224,0,(i+1)*224,76)),(260,318))
  d.text((16,330),'Original stage annotation →',font=small,fill='#555555')
  frames.append(frame)
 frames[-1].save(root/'figures'/f'{name}_poster.png')
 path=root/'figures'/f'{name}.gif'
 frames[0].save(path,save_all=True,append_images=frames[1:],duration=[1000]+[450]*10+[1500],loop=0,disposal=2)
 saved=Image.open(path);assert saved.n_frames==12
 entries.append({'id':name,'title':title,'amplification':amp,'source':dest.name,'sha256':hashlib.sha256(dest.read_bytes()).hexdigest(),'gif':path.name,'frame_count':12,'loop_duration_ms':7000,'encoding':'All twelve original 224×224 image tiles in order, with source held fixed and original stage annotations. No synthesized intermediate images; GIF palette quantization applies.'})
p=root/'figures/animation_manifest.json';data=json.loads(p.read_text());data['closeup_trajectories']=entries;p.write_text(json.dumps(data,indent=2)+'\n')
p=root/'index.html';s=p.read_text();marker='      </div>\n      <p class="animation-note">Cat scores'
assert marker in s
cards=[]
for name,title,amp in cases:
 setting=(f'Amplification {amp} · ' if amp else '')+'12 recorded stages'
 cards.append(f'''      <figure id="showcase-{name}">
        <h4>{title}</h4>
        <p class="example-setting">{setting}</p>
        <div class="fig"><img class="animated" src="figures/{name}.gif" data-gif="figures/{name}.gif" data-still="figures/{name}_poster.png" loading="lazy" width="500" height="402" alt="{title}: all twelve recorded stages, with the unchanged source alongside."></div>
        <figcaption>Original stage labels and scores are retained. <a href="figures/{name}.gif" download>Download GIF</a> · <a href="figures/{name}_strip.png" download>Original sequence</a></figcaption>
      </figure>
''')
if 'id="showcase-cat_closeup"' not in s: p.write_text(s.replace(marker,''.join(cards)+marker))
print('Built and verified six animations, each with twelve recorded stages.')
