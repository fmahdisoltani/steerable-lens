'use strict';
(() => {
  const preference = window.matchMedia('(prefers-reduced-motion: reduce)');
  let playing = !preference.matches;
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
      const item = group[example];
      image.dataset.gif = 'figures/' + item.gif;
      image.dataset.still = 'figures/' + item.poster;
      image.alt = `${item.title}, source ${item.source_id}: actual intermediate optimization steps for Pixel, Fourier phase, CSP phase and Joint CSP, with the original source alongside.`;
      title.textContent = `${item.title} · Source ${item.source_id} · Example ${example + 1} of ${group.length}`;
      timing.textContent = `${item.frame_count} animation frames · ${(item.loop_duration_ms / 1000).toFixed(1)}-second loop`;
      download.href = 'figures/' + item.gif;
      directions.forEach(button => button.setAttribute('aria-pressed', String(button.dataset.celebaDirection === direction)));
      examples.forEach(button => button.setAttribute('aria-pressed', String(Number(button.dataset.celebaExample) === example)));
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
    function selectExample() {
      const item = cases.find(item => item.id === select.value);
      image.dataset.gif = 'figures/' + item.gif;
      image.dataset.still = 'figures/' + item.poster;
      image.alt = `${item.title}: twelve recorded morph frames, with the original source alongside.`;
      title.textContent = item.title;
      timing.textContent = `${item.frame_count} recorded frames · ${(item.loop_duration_ms / 1000).toFixed(1)}-second loop`;
      description.textContent = item.description;
      download.href = 'figures/' + item.gif;
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
    images.forEach(image => {
      const source = playing ? image.dataset.gif : image.dataset.still;
      if (image.getAttribute('src') !== source) image.src = source;
    });
    buttons.forEach(button => {
      button.textContent = playing ? 'Pause animations' : 'Play animations';
      button.setAttribute('aria-pressed', String(playing));
      button.title = playing ? 'Stop GIF playback and show recorded endpoints' : 'Play the recorded image sequence';
    });
  }
  buttons.forEach(button => button.addEventListener('click', () => { playing = !playing; render(); }));
  preference.addEventListener('change', () => { playing = !preference.matches; render(); });
  render();
})();
