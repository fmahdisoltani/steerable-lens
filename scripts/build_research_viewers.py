"""Export exact decoded GIF frames and verified readable stage metadata."""
from pathlib import Path
import json,re,ast
from PIL import Image,ImageDraw
root=Path(__file__).resolve().parents[1];project=root.parent
manifest=json.loads((root/'figures/animation_manifest.json').read_text());assets={r.get('gif'):r for r in manifest['assets']}
labels=[]
for n in ast.parse((project/'venv/lib/python3.9/site-packages/torchvision/models/_meta.py').read_text()).body:
 if isinstance(n,ast.Assign) and any(getattr(t,'id','')=='_IMAGENET_CATEGORIES' for t in n.targets):labels=ast.literal_eval(n.value)
assert len(labels)==1000
pages=['index.html','celeba.html','imagenet.html'];files=set()
for page in pages:
 text=(root/page).read_text();files.update(re.findall(r'data-gif="figures/([^"?]+)',text))
 for id in ['celeba-gallery-data','natural-gallery-data']:
  m=re.search(r'<script[^>]+id="'+id+r'"[^>]*>(.*?)</script>',text,re.S)
  if m:
   for case in json.loads(m[1]):files.add(case.get('comparison',case)['gif'])
meta={}
def describe(r,prefix=''):
 parts=[]
 for k,v in r['scores'].items():
  parts.append(f'{prefix}{k} current prediction: {v.get("label",labels[v["prediction"]])}; target probability: {v["target_probability"]:.3f}')
 if 'l2' in r:parts.append(f'{prefix}image L₂: {r["l2"]:.2f}')
 return ' · '.join(parts)
for filename in sorted(files):
 name=Path(filename).stem;im=Image.open(root/'figures'/filename);entry={'frames':[],'durations':[],'labels':[]};a=assets.get(filename,{})
 if name.startswith('legacy_cat'):
  entry['target']=a['target_label'];stem=name.replace('legacy_','fixed_');records=json.loads((project/f'outputs/website_fixed_gradients/cats/{stem}_live_scores.json').read_text());entry['labels']=[describe(r) for r in records]
 elif name.startswith('comparison_'):
  live=name.removeprefix('comparison_');aa=assets[live+'.gif']
  entry['target']=aa.get('target_label',aa.get('target_class',{}).get('name'))
  if live.startswith('legacy_cat'):
   stem=live.replace('legacy_','fixed_');folder=project/'outputs/website_fixed_gradients/cats';l=json.loads((folder/(stem+'_live_scores.json')).read_text());f=json.loads((folder/(stem+'_scores.json')).read_text())
  else:l=aa['frames'];f=json.loads((project/'outputs/website_fixed_gradients/golf/golf_to_soccer_amp1000_fixed.json').read_text())
  entry['labels']=[describe(x,'Live ')+ '\n'+describe(y,'Fixed ') for x,y in zip(l,f)]
 elif name=='golf_to_soccer_amp1000':entry['target']='soccer ball';entry['labels']=[describe(r) for r in a['frames']]
 elif name=='cat_closeup' or '_face_amp' in name:
  stem='cat3_face_amp120' if name=='cat_closeup' else name
  entry['target']='English springer' if name=='cat_closeup' else 'Egyptian cat'
  entry['labels']=[describe(r) for r in json.loads((project/f'outputs/imagenet_cat_dog_closeups/{stem}.json').read_text())]
 elif name=='dog_recorded_trajectory':entry['target']='Not verified for this supplied strip';entry['labels']=['Current predictions and scores are preserved in the original strip; complete machine-readable metadata is unavailable.']*im.n_frames
 folder=root/'figures/frames'/name;folder.mkdir(parents=True,exist_ok=True)
 for i in range(im.n_frames):
  im.seek(i);frame=im.convert('RGB');entry['durations'].append(im.info.get('duration',400))
  # Natural-image pixels remain untouched; move small raster text into readable HTML.
  if name.startswith('comparison_'):frame=frame.crop((0,99,frame.width,323));entry['columns']=['Source (fixed)','Live gradient','Fixed gradient']
  elif name.startswith('legacy_cat'):frame=frame.crop((0,88,500,312));entry['columns']=['Source (fixed)','Live gradient']
  elif name in ['golf_to_soccer_amp1000','cat_closeup','dog_recorded_trajectory'] or '_face_amp' in name:frame=frame.crop((0,90,500,314));entry['columns']=['Source (fixed)','Recorded edit']
  elif name.startswith('celeba_'):
   ImageDraw.Draw(frame).rectangle((200,327,959,348),fill='white');entry['endpointNote']='Endpoint interpretation: “Both evaluation classifiers predict target” means O and O₂ both predict the intended target; it is not a human rating.'
  elif name=='main_morph_sequence':
   d=ImageDraw.Draw(frame)
   for y in [333,639]:d.rectangle((200,y,959,y+21),fill='white')
   entry['endpointNote']='Both evaluation classifiers predict target: MNIST — Pixel yes, Fourier phase no, CSP phase no, Joint CSP no. CelebA — Pixel yes, Fourier phase no, CSP phase yes, Joint CSP yes. These are recorded endpoint results, not human ratings.'
  path=folder/f'{i:03d}.webp';frame.save(path,lossless=True)
  # Lossless export must preserve all retained pixels exactly.
  assert Image.open(path).convert('RGB').tobytes()==frame.tobytes()
  entry['frames'].append(str(path.relative_to(root)))
 if entry.get('columns'):
  frame0=Image.open(folder/'000.webp');box=(16,0,240,224);frame0.crop(box).resize((72,72)).save(root/'figures'/f'{name}_thumb.png')
 meta[filename]=entry
fits=[json.loads(line) for line in (project/'outputs/celeba_structure_margin_seed20260923/evaluation/fits.jsonl').read_text().splitlines()]
fits={(r['id'],r['method']):r for r in fits if r['budget']==128/28 and r['grid']==8 and r['gain']}
names={'pixel':'Pixel','fourier_phase':'Fourier phase','csp_phase':'CSP phase','csp_joint':'Joint CSP'}
for filename,entry in meta.items():
 if filename.startswith('celeba_'):
  a=assets[filename]; parts=[]
  records={inp['method']:json.loads((project/Path(inp['recorded_npz']).with_suffix('.json')).read_text())['frames'] for inp in a['inputs']}
  entry['target']=a['title']
  entry['labels']=[' · '.join(f"{names[method]}: step {records[method][idx]['step']}, L₂ {records[method][idx]['l2']:.2f}, G target probability {records[method][idx]['target_probability']:.3f}" for method,idx in mapping.items()) for mapping in a['frame_map']]

  for inp in a['inputs']:
   r=fits[a['id'],inp['method']];joint=all(r['scores'][k]['prediction']==r['target'] for k in ['O','O2'])
   parts.append(f"{names[inp['method']]}: {'yes' if joint else 'no'}; E {r['explained']*100:.1f}%")
  entry['endpointNote']='Endpoint only — Both evaluation classifiers predict target; E is warp-plus-gain explained energy. '+ ' · '.join(parts)
 if filename=='main_morph_sequence.gif':
  entry['endpointNote']+=' Endpoint warp-plus-gain E (Pixel / Fourier phase / CSP phase / Joint CSP): MNIST 49.0% / 34.0% / 64.5% / 70.4%; CelebA 6.1% / 69.8% / 67.3% / 64.5%.'
(root/'assets/frame_players.json').write_text(json.dumps(meta,separators=(',',':')))
print('Exported',sum(len(x['frames']) for x in meta.values()),'lossless frames for',len(meta),'sequences.')
