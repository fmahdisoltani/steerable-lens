"""Count observed attainment; never substitute zeros for missing fit quality."""
from pathlib import Path
import json,hashlib
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
root=Path(__file__).resolve().parents[1];src=root.parent/'outputs/celeba_structure_margin_seed20260923/evaluation'
p=src/'endpoints.jsonl';records=[json.loads(l) for l in p.read_text().splitlines()];summary=json.loads((src/'summary.json').read_text())
methods=['pixel','fourier_phase','csp_phase','csp_joint'];budgets=sorted({r['budget'] for r in records});tasks=[('Smiling',0,'Add smile'),('Smiling',1,'Remove smile'),('Eyeglasses',0,'Add glasses'),('Eyeglasses',1,'Remove glasses')]
rows=[]
for attr,source,label in tasks:
 for b in budgets:
  rs=[r for r in records if r['attribute']==attr and r['source']==source and r['budget']==b];ids={r['id'] for r in rs};assert len(ids)==25
  lookup={(r['id'],r['method']):r for r in rs};assert len(lookup)==100
  counts={m:sum(lookup[i,m]['attained'] for i in ids) for m in methods}
  common=sorted(i for i in ids if all(lookup[i,m]['attained'] for m in methods))
  ns={r['n'] for r in summary if r['attribute']==attr and r['source']==source and r['budget']==b};assert ns=={len(common)},(label,b,ns,len(common))
  rows.append({'task':label,'budget':b,'requested':len(ids),'common_attained':len(common),'per_method_attained':counts,'common_case_ids':common})
(root/'assets/celeba_coverage.json').write_text(json.dumps({'source_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'definition':'Common attainment requires all four methods to attain the requested distance for the same source-target case at that budget. Unattained cases are excluded from conditional reconstruction summaries, not assigned zero quality.','rows':rows},indent=2)+'\n')
plt.rcParams.update({'font.size':11,'svg.fonttype':'none'})
fig,axes=plt.subplots(1,4,figsize=(11,2.9),sharey=True)
for ax,(_,_,task) in zip(axes,tasks):
 rs=[r for r in rows if r['task']==task];ys=[r['common_attained'] for r in rs]
 ax.plot([0,1],ys,'o-',color='#99512d',lw=1.5)
 for x,y in enumerate(ys):ax.annotate(f'{y}/25',(x,y),xytext=(0,9),textcoords='offset points',ha='center',fontweight='bold')
 ax.set_title(task);ax.set_xticks([0,1],['64/28\n≈ 2.29','128/28\n≈ 4.57']);ax.set_xlim(-.3,1.3);ax.set_ylim(0,29);ax.set_yticks([0,5,10,15,20,25]);ax.grid(axis='y',alpha=.18);ax.set_axisbelow(True);ax.spines[['top','right']].set_visible(False);ax.set_xlabel('Requested image L₂')
axes[0].set_ylabel('Cases attained by all 4 methods')
fig.tight_layout()
for ext in ['svg','png']:fig.savefig(root/f'figures/celeba_coverage.{ext}',dpi=180,bbox_inches='tight')
print([(r['task'],round(r['budget'],2),r['common_attained']) for r in rows])
