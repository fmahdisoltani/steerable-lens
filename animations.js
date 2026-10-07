'use strict';
(() => {
  let frameData = null;
  const players = new Map();
  const preference = window.matchMedia('(prefers-reduced-motion: reduce)');
  const images = [...document.querySelectorAll('img.animated')];
  const buttons = [...document.querySelectorAll('.motion-toggle')];
  const galleryData = document.getElementById('celeba-gallery-data');
  if (galleryData) {
    const cases = JSON.parse(galleryData.textContent);
    const image = document.getElementById('celeba-morph');
    const directions = [...document.querySelectorAll('[data-celeba-direction]')];
    const examples = [...document.querySelectorAll('[data-celeba-example]')];
    const title = document.getElementById('celeba-case-title');
    const timing = document.getElementById('celeba-case-timing');
    const download = document.getElementById('celeba-download');
    let direction = cases[0].group;
    let example = 0;
    function selectCase() {
      const group = cases.filter(item => item.group === direction);
      example = Math.min(example, group.length - 1);
      const item = group[example];
      image.dataset.gif = 'figures/' + item.gif;
      image.dataset.still = 'figures/' + item.poster;
      image.alt = `${item.title}, source ${item.source_id}: actual intermediate optimization steps for Pixel, Fourier phase, CSP phase and Joint CSP, with the original source alongside.`;
      title.textContent = `${item.title} · Source ${item.source_id} · Example ${example + 1} of ${group.length}`;
      timing.textContent = `${item.frame_count} animation frames · ${(item.loop_duration_ms / 1000).toFixed(1)}-second loop`;
      download.href = 'figures/' + item.gif;
      directions.forEach(button => button.setAttribute('aria-pressed', String(button.dataset.celebaDirection === direction)));
      examples.forEach(button => {
        button.hidden = Number(button.dataset.celebaExample) >= group.length;
        button.setAttribute('aria-pressed', String(Number(button.dataset.celebaExample) === example));
      });
      render();
    }
    directions.forEach(button => button.addEventListener('click', () => {
      direction = button.dataset.celebaDirection;
      example = 0;
      selectCase();
    }));
    examples.forEach(button => button.addEventListener('click', () => {
      example = Number(button.dataset.celebaExample);
      selectCase();
    }));
    selectCase();
  }
  const naturalData = document.getElementById('natural-gallery-data');
  if (naturalData) {
    const cases = JSON.parse(naturalData.textContent);
    const sources = [...document.querySelectorAll('[data-natural-source]')];
    const select = document.getElementById('natural-example');
    const image = document.getElementById('natural-morph');
    const title = document.getElementById('natural-case-title');
    const timing = document.getElementById('natural-case-timing');
    const description = document.getElementById('natural-case-description');
    const download = document.getElementById('natural-download');
    const fixedDownload = document.getElementById('natural-fixed-download');
    const liveDownload = document.getElementById('natural-live-download');
    function selectExample() {
      const item = cases.find(item => item.id === select.value);
      image.dataset.gif = 'figures/' + item.comparison.gif;
      image.dataset.still = 'figures/' + item.comparison.poster;
      image.alt = `${item.title}: source, live-gradient and fixed-gradient sequences shown together over twelve synchronized frames.`;
      title.textContent = item.title;
      timing.textContent = `${item.frame_count} recorded frames · ${(item.loop_duration_ms / 1000).toFixed(1)}-second loop`;
      description.textContent = item.comparison.description;
      download.href = 'figures/' + item.comparison.gif;
      fixedDownload.href = 'figures/' + item.fixed.gif;
      liveDownload.href = 'figures/' + item.gif;
      render();
    }
    function selectSource(group) {
      select.replaceChildren();
      cases.filter(item => item.group === group).forEach(item => {
        const option = document.createElement('option');
        option.value = item.id;
        option.textContent = item.option_label;
        select.appendChild(option);
      });
      sources.forEach(button => button.setAttribute('aria-pressed', String(button.dataset.naturalSource === group)));
      selectExample();
    }
    sources.forEach(button => button.addEventListener('click', () => selectSource(button.dataset.naturalSource)));
    select.addEventListener('change', selectExample);
    selectSource(cases[0].group);
  }
  function render() {
    if (!frameData) return;
    images.forEach(image => {
      const key = image.dataset.gif.split('/').pop().split('?')[0];
      const data = frameData[key];
      if (!data || players.get(image)?.key === key) return;
      players.get(image)?.stop();
      image.parentElement.parentElement.querySelector('.frame-controls')?.remove();
      image.parentElement.querySelector('.frame-columns')?.remove();
      const columns = document.createElement('div'); columns.className = 'frame-columns';
      (data.columns || []).forEach(label => { const span=document.createElement('span');span.textContent=label;columns.append(span); });
      if (data.columns) { columns.style.gridTemplateColumns=`repeat(${data.columns.length},1fr)`;image.before(columns);image.style.height='auto';image.removeAttribute('height'); }
      const box=document.createElement('div');box.className='frame-controls';
      const target=document.createElement('p');target.className='frame-target';target.textContent=data.target ? `Intended target: ${data.target}` : 'Recorded optimization sequence';
      const row=document.createElement('div');row.className='frame-buttons';
      const button=label=>{const b=document.createElement('button');b.type='button';b.textContent=label;row.append(b);return b;};
      const play=button('Play');
      const slider=document.createElement('input');slider.type='range';slider.min=0;slider.max=data.frames.length-1;slider.value=0;slider.setAttribute('aria-label','Recorded frame');
      const status=document.createElement('p');status.className='frame-status';
      const note=document.createElement('p');note.className='small-note';note.textContent=data.endpointNote || '';
      const frameLabel=document.createElement('label');frameLabel.textContent='Recorded frame · source → final';frameLabel.append(slider);
      box.append(target,row,frameLabel,status,note);image.parentElement.after(box);
      const ampMatch=key.match(/^(.*_amp)([0-9]+)\.gif$/);
      if(ampMatch){
        const variants=Object.keys(frameData).map(k=>({key:k,match:k.match(/^(.*_amp)([0-9]+)\.gif$/)})).filter(v=>v.match&&v.match[1]===ampMatch[1]).sort((a,b)=>Number(a.match[2])-Number(b.match[2]));
        const ampLabel=document.createElement('label'),amp=document.createElement('input');amp.type='range';amp.min=0;amp.max=Math.max(1,variants.length-1);amp.step=1;amp.value=variants.findIndex(v=>v.key===key);amp.disabled=variants.length<2;const ampText=document.createElement('span');ampText.textContent=`Amplification: ${ampMatch[2]}${amp.disabled?' (only recorded setting)':' · recorded settings '+variants.map(v=>v.match[2]).join(', ')}`;ampLabel.append(ampText,amp);amp.setAttribute('aria-label','Recorded amplification');amp.setAttribute('aria-valuetext',ampMatch[2]);box.insertBefore(ampLabel,frameLabel);
        amp.oninput=()=>{stop();const next=variants[Number(amp.value)];image.dataset.gif='figures/'+next.key;const dropdown=document.getElementById('natural-example');const optionValue=next.key.replace(/^comparison_/,'').replace(/\.gif$/,'');if(image.id==='natural-morph'&&dropdown&&[...dropdown.options].some(o=>o.value===optionValue)){dropdown.value=optionValue;dropdown.dispatchEvent(new Event('change'));}else{image.dataset.still='figures/'+next.key.replace('.gif','_poster.png');image.alt=`${data.target}: amplification ${next.match[2]}, recorded sequence`;const figure=image.closest('figure');const setting=figure?.querySelector('.example-setting');if(setting)setting.textContent='Amplification '+next.match[2];const link=figure?.querySelector('a[download]');if(link)link.href='figures/'+next.key;render();}};
      }
      const distances=data.labels.map(text=>[...text.matchAll(/(?:image )?L₂:? ([0-9.]+)/g)].map(m=>Number(m[1])));
      let distanceSlider=null,distanceOutput=null,reference=null;
      if(distances.length===data.frames.length&&distances.every(v=>v.length&&v.every(Number.isFinite))){
        const budgetLabel=document.createElement('label');distanceOutput=document.createElement('span');distanceSlider=document.createElement('input');distanceSlider.type='range';distanceSlider.min=0;distanceSlider.step='any';distanceSlider.setAttribute('aria-label','Image distance L2, nearest recorded frame');
        const count=distances[0].length;reference=document.createElement('select');reference.setAttribute('aria-label','Distance reference');const names=count===4?['Pixel','Fourier phase','CSP phase','Joint CSP']:count===2?['Live gradient','Fixed gradient']:['Recorded edit'];names.forEach((name,i)=>{const option=document.createElement('option');option.value=i;option.textContent=name;reference.append(option);});
        budgetLabel.append(distanceOutput);if(count>1)budgetLabel.append(reference);budgetLabel.append(distanceSlider);box.insertBefore(budgetLabel,status);
        const hint=document.createElement('p');hint.className='small-note';hint.textContent='Image distance selects the nearest recorded frame, not a new optimization budget. Other methods may have different distances at that frame; no interpolation is applied.';box.insertBefore(hint,status);
        reference.onchange=()=>{stop();show(index);};distanceSlider.oninput=()=>{stop();const ref=Number(reference.value),desired=Number(distanceSlider.value);let closest=0;distances.forEach((v,i)=>{if(Math.abs(v[ref]-desired)<Math.abs(distances[closest][ref]-desired))closest=i;});show(closest);};
      }
      let index=0,timer=null,running=!preference.matches,request=0;
      const stop=()=>{running=false;++request;clearTimeout(timer);play.textContent='Play';};
      const show=(n)=>{index=n;const token=++request;const preload=new Image();preload.onload=()=>{if(token!==request)return;image.src=preload.src;slider.value=n;if(distanceSlider){const ref=Number(reference.value);distanceSlider.max=Math.max(...distances.map(v=>v[ref]));distanceSlider.value=distances[n][ref];distanceOutput.textContent=`Image distance (L₂): ${distances[n][ref].toFixed(2)} · ${reference.options[ref].textContent}`;}status.textContent=`Frame ${n+1} of ${data.frames.length}\n${data.labels[n] || ''}`;if(running)timer=setTimeout(()=>show((n+1)%data.frames.length),data.durations[n] || 400);};preload.onerror=()=>{stop();status.textContent='Frame could not load. Try again or download the original GIF.';};preload.src=data.frames[n];};
      play.onclick=()=>{if(running)stop();else{running=true;play.textContent='Pause';show(index);}};
      slider.oninput=()=>{stop();show(Number(slider.value));};
      players.set(image,{key,stop});play.textContent=running?'Pause':'Play';show(0);
    });
  }
  buttons.forEach(button => button.remove());
  fetch('assets/frame_players.json').then(r=>{if(!r.ok)throw new Error('Frame metadata unavailable');return r.json();}).then(data=>{frameData=data;render();}).catch(()=>{});
  preference.addEventListener('change',()=>{if(preference.matches)players.forEach(p=>p.stop());});
})();
