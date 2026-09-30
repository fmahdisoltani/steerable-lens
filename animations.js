'use strict';
(() => {
  const preference = window.matchMedia('(prefers-reduced-motion: reduce)');
  let playing = !preference.matches;
  const images = [...document.querySelectorAll('img.animated')];
  const buttons = [...document.querySelectorAll('.motion-toggle')];
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
