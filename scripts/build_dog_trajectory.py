"""Animate the twelve supplied panels without interpolating their image pixels."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import hashlib, json, shutil, sys
root=Path(__file__).resolve().parents[1]
source=Path(sys.argv[1]) if len(sys.argv)>1 else root/'figures/dog_recorded_trajectory_strip.png'
dest=root/'figures/dog_recorded_trajectory_strip.png'
if source.resolve()!=dest.resolve(): shutil.copyfile(source,dest)
im=Image.open(dest).convert('RGB')
assert im.size==(2688,288),im.size
font=ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial.ttf',16)
small=ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial.ttf',13)
frames=[]
for i in range(12):
 frame=Image.new('RGB',(500,390),'white');d=ImageDraw.Draw(frame)
 d.text((16,12),'Dog · recorded trajectory',font=font,fill='#222222')
 d.text((16,38),'Twelve supplied stages · no interpolated images',font=small,fill='#555555')
 d.text((75,68),'Source (fixed)',font=small,fill='#222222')
 d.text((315,68),f'Stage {i+1} of 12',font=small,fill='#222222')
 frame.paste(im.crop((0,64,224,288)),(16,90))
 frame.paste(im.crop((i*224,64,(i+1)*224,288)),(260,90))
 frame.paste(im.crop((i*224,0,(i+1)*224,64)),(260,318))
 d.text((16,330),'Original stage annotation →',font=small,fill='#555555')
 frames.append(frame)
frames[-1].save(root/'figures/dog_recorded_trajectory_poster.png')
frames[0].save(root/'figures/dog_recorded_trajectory.gif',save_all=True,append_images=frames[1:],duration=[1000]+[450]*10+[1500],loop=0,disposal=2)
p=root/'figures/animation_manifest.json';data=json.loads(p.read_text());data['additional_dog_trajectory']={'source':'dog_recorded_trajectory_strip.png','sha256':hashlib.sha256(dest.read_bytes()).hexdigest(),'gif':'dog_recorded_trajectory.gif','frame_count':12,'loop_duration_ms':7000,'encoding':'Exact 224×224 tiles from supplied strip, in order; source held fixed; original stage annotations retained. GIF palette quantization applies. Target, amplification, and gradient-refresh configuration are not independently established for this supplied strip.'};p.write_text(json.dumps(data,indent=2)+'\n')
