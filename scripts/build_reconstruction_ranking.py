"""Render descriptive medians from the public data without inferring uncertainty."""
from pathlib import Path
import json
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
root=Path(__file__).resolve().parents[1]
rows=[r for r in json.loads((root/'data.json').read_text())['charts'] if r['dataset']=='CelebA']
plt.rcParams.update({'font.size':11,'svg.fonttype':'none'})
fig,axes=plt.subplots(1,2,figsize=(11,4.3),sharex=True,sharey=True)
colors={'fourier_phase':'#3579a8','csp_phase':'#a95728'}
for ax,fit,title in zip(axes,['warp','gain'],['Warp only','Warp + gain']):
 for i,r in enumerate(rows):
  values={x['key']:x['e'] for x in r['fits'][fit]}
  ax.plot([values['fourier_phase']*100,values['csp_phase']*100],[i-.12,i+.12],color='#bdbdbd',lw=2,zorder=1)
  for method,offset,marker in [('fourier_phase',-.12,'o'),('csp_phase',.12,'s')]:
   v=values[method]*100
   ax.scatter(v,i+offset,color=colors[method],marker=marker,s=48,zorder=3)
   ax.annotate(f'{v:.1f}',(v,i+offset),xytext=(7,0),textcoords='offset points',va='center',fontsize=9,color=colors[method])
 ax.set_title(title,fontweight='bold',pad=14);ax.set_xlim(0,90);ax.set_xticks([0,20,40,60,80]);ax.grid(axis='x',alpha=.2);ax.set_axisbelow(True)
 ax.set_xlabel('Median explained edit energy (%)')
 ax.spines[['top','right','left']].set_visible(False);ax.tick_params(axis='y',length=0)
axes[0].set_yticks(range(4),[f'{r["title"]}\n{r["n"]}/{r["requested"]} cases' for r in rows]);axes[0].invert_yaxis()
fig.legend(handles=[Line2D([],[],color=c,marker=m,linestyle='',label=n) for c,m,n in [(colors['fourier_phase'],'o','Fourier phase'),(colors['csp_phase'],'s','CSP phase')]],loc='upper center',ncol=2,frameon=False)
fig.tight_layout(rect=[0,0,1,.91],w_pad=4)
fig.savefig(root/'figures/reconstruction_ranking.svg',bbox_inches='tight')
fig.savefig(root/'figures/reconstruction_ranking.png',dpi=180,bbox_inches='tight')
