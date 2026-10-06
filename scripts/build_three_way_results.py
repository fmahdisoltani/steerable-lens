"""Matched-budget summaries and paired source-cluster bootstrap from recorded results."""
from pathlib import Path
import json, hashlib
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
root=Path(__file__).resolve().parents[1]
src=root.parent/'outputs/mnist_test_structure_replication_seed20260923'
read=lambda p:[json.loads(l) for l in p.read_text().splitlines() if l.strip()]
ends=read(src/'endpoints.jsonl');fits=read(src/'fits.jsonl')
methods=['pixel','fourier_phase','csp_phase','csp_joint'];names=['Pixel','Fourier phase','CSP phase','Joint CSP'];budgets=[1.,2.]
lookup={(r['id'],r['method'],r['budget']):r for r in ends};assert len(lookup)==len(ends)
fit={(r['id'],r['method'],r['budget'],r['gain']):r for r in fits if r['grid']==8}
cases=sorted({r['id'] for r in ends});assert len(cases)==300
source={r['id']:r['index'] for r in ends};clusters=sorted(set(source.values()));groups=[np.array([i for i,c in enumerate(cases) if source[c]==s]) for s in clusters]
rng=np.random.default_rng(20261006);draws=[np.concatenate([groups[i] for i in row]) for row in rng.integers(0,len(groups),(2000,len(groups)))]
metrics=['driver_probability','O_success','O2_success','joint_success','warp','warp_gain']
results=[];replicates={}
for b in budgets:
 for m in methods:
  rs=[lookup[c,m,b] for c in cases]
  assert all(r['attained'] for r in rs)
  vals=np.array([[r['scores']['G']['target_probability'],r['scores']['O']['prediction']==r['target'],r['scores']['O2']['prediction']==r['target'],all(r['scores'][k]['prediction']==r['target'] for k in ['O','O2']),fit[r['id'],m,b,False]['explained'],fit[r['id'],m,b,True]['explained']] for r in rs],dtype=float)
  def reduce(a):return np.array([np.median(a[:,0]),*np.mean(a[:,1:4],axis=0),*np.median(a[:,4:],axis=0)])
  point=reduce(vals);boot=np.array([reduce(vals[ix]) for ix in draws]);replicates[b,m]=boot
  ci=np.quantile(boot,[.025,.975],axis=0)
  r={'budget':b,'method':m,'evaluated':len(rs),'requested':len(cases),'attained':sum(x['attained'] for x in rs),'metrics':{k:{'estimate':float(point[j]),'ci95':[float(ci[0,j]),float(ci[1,j])]} for j,k in enumerate(metrics)},'success_counts':{k:int(vals[:,j].sum()) for j,k in enumerate(metrics) if j in [1,2,3]}}
  results.append(r)
# Verify source summaries before writing new displays.
reference=json.loads((src/'summary.json').read_text())
for r in results:
 q=next(q for q in reference if q['budget']==r['budget'] and q['method']==r['method'] and q['grid']==8)
 assert abs(r['metrics']['driver_probability']['estimate']-q['G'])<1e-12
 assert abs(r['metrics']['warp_gain']['estimate']-q['warp_gain'])<1e-12
 assert r['success_counts']['joint_success']==q['joint_count']
paired=[]
for b in budgets:
 for i,m in enumerate(methods):
  for n in methods[i+1:]:
   a=next(r for r in results if r['budget']==b and r['method']==m);z=next(r for r in results if r['budget']==b and r['method']==n)
   delta=replicates[b,m]-replicates[b,n];ci=np.quantile(delta,[.025,.975],axis=0)
   paired.append({'budget':b,'contrast':m+' minus '+n,'metrics':{k:{'estimate':a['metrics'][k]['estimate']-z['metrics'][k]['estimate'],'ci95':[float(ci[0,j]),float(ci[1,j])]} for j,k in enumerate(metrics)}})
metadata={'dataset':'MNIST','source_count':len(clusters),'bootstrap_draws':2000,'seed':20261006,'interval':'Pointwise 95% percentile source-cluster bootstrap; identical draws across methods and budgets. All target cases of a sampled source are retained together. Current data contain 300 distinct source images. Conditional on trained models; not multiplicity-adjusted. Zero observed successes yield degenerate bootstrap intervals, not proof of zero population success.','reconstruction':'Median explained energy, 8x8 grid, warp only and warp plus gain.','sources':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in [src/'endpoints.jsonl',src/'fits.jsonl']},'results':results,'paired_method_differences':paired}
(root/'assets/three_way_results.json').write_text(json.dumps(metadata,indent=2)+'\n')
plt.rcParams.update({'font.size':10,'svg.fonttype':'none'})
fig,axes=plt.subplots(2,3,figsize=(13.5,7.6),sharex=True,sharey=True)
styles=[ [('driver_probability','G probability','#66509a','o',0)], [('O_success','O','#3277a5','o',-.20),('O2_success','O₂','#bb7028','s',0),('joint_success','Both','#343434','D',.20)], [('warp','Warp only','#288277','o',-.12),('warp_gain','Warp + gain','#b05a7f','s',.12)] ]
for row,b in enumerate(budgets):
 for col,series in enumerate(styles):
  ax=axes[row,col]
  for i,m in enumerate(methods):
   r=next(r for r in results if r['budget']==b and r['method']==m)
   for key,label,color,marker,off in series:
    v=r['metrics'][key];x=v['estimate']*100;lo,hi=np.array(v['ci95'])*100
    ax.plot([lo,hi],[i+off,i+off],color=color,lw=1.5)
    ax.scatter(x,i+off,c=color,marker=marker,s=30,zorder=3,clip_on=False)
  ax.set_xlim(0,100);ax.set_xticks([0,25,50,75,100]);ax.grid(axis='x',alpha=.18);ax.set_axisbelow(True);ax.spines[['top','right']].set_visible(False)
  ax.set_xlabel(['Median target probability (%)','Target-success rate (%)','Median explained edit energy (%)'][col]);ax.tick_params(axis='x',labelbottom=True)
  if row==0:
   ax.set_title(['Optimized confidence','Evaluation-classifier transfer','Smooth reconstruction'][col],fontweight='bold',pad=40)
   ax.legend(handles=[Line2D([],[],marker=marker,color=color,linestyle='',label=label) for _,label,color,marker,_ in series],loc='lower center',bbox_to_anchor=(.5,1.015),ncol=3,frameon=False,fontsize=9)
 axes[row,0].set_yticks(range(4),names);axes[row,0].set_ylabel(f'L₂ = {b:g}\nEvaluated: 300 per method\nAttained: 300/300 per method',labelpad=15)
axes[0,0].set_ylim(3.5,-.5)
fig.tight_layout(h_pad=3,w_pad=2)
for ext in ['svg','png']:fig.savefig(root/f'figures/three_way_results.{ext}',dpi=180,bbox_inches='tight')
# Render accessible exact counts and estimates for both budgets.
tables=[]
for b in budgets:
 trs=''
 for m,name in zip(methods,names):
  r=next(r for r in results if r['budget']==b and r['method']==m);v=r['metrics'];ct=r['success_counts']
  prob=v['driver_probability']['estimate']*100;probtext=f'{prob:.1f}%' if prob>=1 else f'{prob:.4g}%'
  trs+=f'<tr><th scope="row">{name}</th><td>{probtext}</td><td>{ct["O_success"]}/300</td><td>{ct["O2_success"]}/300</td><td>{ct["joint_success"]}/300</td><td>{v["warp"]["estimate"]*100:.1f}%</td><td>{v["warp_gain"]["estimate"]*100:.1f}%</td><td>300</td><td>300/300</td></tr>'
 tables.append(f'<div class="result-table" tabindex="0" role="region" aria-label="Exact results at L2 {b:g}"><table><caption>MNIST · L₂ = {b:g}</caption><thead><tr><th>Method</th><th>Median G probability</th><th>O target</th><th>O₂ target</th><th>Both target</th><th>Median E: warp</th><th>Median E: warp + gain</th><th>Evaluated</th><th>Attained / requested</th></tr></thead><tbody>{trs}</tbody></table></div>')
section='''<section id="findings"><h2>Confidence, transfer, and reconstruction give different answers</h2>
<p>The same 300 MNIST source images are evaluated at two recorded image-distance budgets. Driver confidence, transfer to other classifiers, and smooth reconstruction measure different outcomes; no column certifies recognizable target-class change.</p>
<figure><div class="fig quantitative-figure" tabindex="0" aria-label="Three-way results at two budgets; scroll horizontally on narrow screens"><img loading="lazy" src="figures/three_way_results.svg" alt="Two rows compare image L2 budgets 1 and 2. Four methods align across separate confidence, transfer, and reconstruction axes. At budget 2, pixel median driver confidence is 96.2%, but both evaluation classifiers predict the target on only 10 of 300 cases. All methods attain both budgets on all 300 cases."></div><figcaption>Points show medians for probability and reconstruction, and proportions for target prediction by O, O₂, and both. Bars are pointwise 95% source-cluster bootstrap intervals (2,000 draws), with the same resampled sources across methods and budgets. Reconstruction uses an 8×8 grid. Both recorded budgets are shown; there is no interpolation between them. <a href="figures/three_way_results.svg" download>Download figure</a>.</figcaption></figure>
<p>At L₂ = 2, pixel edits reach median driver target probability 96.2%, while both evaluation classifiers predict the target on 10/300 edits. Joint target counts are 3/300 for Fourier phase, 6/300 for CSP phase, and 8/300 for Joint CSP. The CSP variants have greater median smooth-reconstruction compatibility at this budget.</p>
<details class="details-note"><summary>Exact counts, denominators, and both budgets</summary>'''+''.join(tables)+'''</details>
<details class="details-note"><summary>Uncertainty and scope</summary><p>Sources are the resampling unit, preserving all observations from a source across methods and budgets. These data contain 300 distinct source images. The downloadable paired method differences use the same bootstrap draws; separate marginal intervals should not be used as a test of a paired difference. Intervals are conditional on the trained models, pointwise, and not adjusted for multiple comparisons. Zero observed successes produce a zero-width percentile-bootstrap interval; this does not establish a zero population success rate. Attainment is 300/300 for every method at both budgets, so no cases are excluded here.</p></details>
<p class="small-note"><a href="assets/three_way_results.json" download>Estimates, intervals, paired differences, and provenance</a> · <a href="explore.html#results">Explore reconstruction results</a></p></section>'''
p=root/'index.html';s=p.read_text();import re
s,n=re.subn(r'<section id="findings">.*?</section>',lambda _:section,s,flags=re.S);assert n==1
p.write_text(s.replace('narrative.css?v=reordered-5','narrative.css?v=quantitative-6'))
print('Verified all medians and joint counts against saved summary; generated two-budget figure and paired intervals.')
