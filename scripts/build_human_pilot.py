"""Publish descriptive aggregates only; never export response text or timestamps."""
from pathlib import Path
import json,re,hashlib
root=Path(__file__).resolve().parents[1];src=root.parent/'outputs/celeba_human90_seed20260925'
p=src/'human_summary.json';data=json.loads(p.read_text());rows=data['rows'];assert len(rows)==180
assert {r['rater_id'] for r in rows}=={'rater1','rater2'}
sets=[{r['item_id'] for r in rows if r['rater_id']==k} for k in ['rater1','rater2']];assert sets[0]==sets[1] and len(sets[0])==90
assert len({(r['rater_id'],r['item_id']) for r in rows})==180
assert len({r['source_id'] for r in rows})==24
methods=[('pixel','Pixel'),('fourier_phase','Fourier phase'),('csp_phase','CSP phase'),('csp_joint','Joint CSP')]
results=[];tables=[];ref={r['method']:r for r in json.loads((src/'two_rater_analysis.json').read_text())['methods']}
for metric,field,value,title in [('clear','attribute','clear','Clear intended attribute change'),('no_corruption','corruption','none','No visible corruption')]:
 trs=''
 for method,name in methods:
  cells=[]
  for rater,label in [('rater1','Rater A'),('rater2','Rater B'),(None,'Pooled')]:
   rs=[r for r in rows if r['method']==method and (rater is None or r['rater_id']==rater)]
   n=len(rs);count=sum(r[field]==value for r in rs)
   if rater is None:assert count==ref[method][metric] and n==ref[method]['n']
   results.append({'outcome':metric,'method':method,'rater':label,'count':count,'denominator':n,'proportion':count/n})
   cells.append(f'<td>{count}/{n} <span class="small-note">({count/n*100:.1f}%)</span></td>')
  trs+='<tr><th scope="row">'+name+'</th>'+''.join(cells)+'</tr>'
 tables.append('<div class="result-table" tabindex="0" role="region" aria-label="'+title+' by rater"><table><caption>'+title+'</caption><thead><tr><th scope="col">Method</th><th scope="col">Rater A</th><th scope="col">Rater B</th><th scope="col">Pooled ratings</th></tr></thead><tbody>'+trs+'</tbody></table></div>')
(root/'assets/human_pilot_descriptive.json').write_text(json.dumps({'study':'Original two-rater CelebA pilot','raters':2,'edited_images':90,'source_attribute_cases':24,'ratings':180,'source_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'scope':'Convenience sample; descriptive proportions only. Each rater evaluated the same 90 edited images. Pooled denominators count ratings, not independent images or participants. Future website responses are a separate study and are not included.','results':results},indent=2)+'\n')
section='''<section id="human-pilot"><h2>What did two raters report? An exploratory pilot</h2>
<p>Two voluntary friends-and-family raters each evaluated the same 90 edited images from 24 source–attribute cases, yielding 180 ratings. This convenience sample describes responses to these selected edits; it does not establish a population-level perceptual advantage for any method.</p>
'''+''.join(tables)+'''
<p class="small-note">Each cell reports the number choosing that response divided by all ratings for that method, followed by the proportion. Each rater assessed 23 Pixel, 23 Fourier-phase, 22 CSP-phase, and 22 Joint-CSP edits. Pooled denominators count two ratings per edited image, not independent images or participants. The two outcomes are separate questions; their counts should not be added.</p>
<p>The raters differ in their judgments. For clear attribute change, Rater A reports 13/22 for CSP phase and 10/22 for Joint CSP; Rater B reports 7/22 and 12/22, respectively. These descriptive results do not support a stable ranking between the two CSP variants or demonstrate that an automated metric predicts human perception.</p>
<p><a href="assets/human_pilot_descriptive.json" download>Download per-rater and pooled descriptive counts</a></p>
<details class="details-note"><summary>What a follow-up study should establish</summary><p>A stronger study would use a prespecified image sample, blinded method labels, randomized presentation, and more independently recruited raters. Analysis should account for repeated ratings of images and repeated responses from each rater. This is a proposed follow-up, not a completed validation.</p><p>Any future public website questionnaire responses belong to a separate study and are not included above. Visitors may have seen labeled demonstrations, and participation is self-selected; those responses should not be pooled with the original pilot or treated as blinded validation.</p></details>
</section>'''
p=root/'index.html';s=p.read_text();s,n=re.subn(r'<section id="human-pilot">.*?</section>',lambda _:section,s,flags=re.S);assert n==1;p.write_text(s)
print('Verified both 90-item rating sets and all pooled counts; exported aggregates only.')
