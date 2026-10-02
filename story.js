/* Reading navigation and the coordinate-space explainer. */
(() => {
  "use strict";

  const coordinateLabels = {
    pixel: "Pixel intensities",
    fourier: "Global Fourier phase",
    csp: "Local multiscale phase",
    joint: "Local phase + amplitude",
  };
  const methodButtons = Array.from(document.querySelectorAll("[data-method]"));
  const methodPanels = Array.from(document.querySelectorAll("[data-method-panel]"));
  const coordinateLabel = document.getElementById("method-coordinate");

  function selectMethod(method) {
    if (!Object.hasOwn(coordinateLabels, method) ||
        !methodPanels.some(panel => panel.dataset.methodPanel === method)) return;

    methodButtons.forEach(button => {
      button.setAttribute("aria-pressed", String(button.dataset.method === method));
    });
    methodPanels.forEach(panel => {
      panel.hidden = panel.dataset.methodPanel !== method;
    });
    if (coordinateLabel) coordinateLabel.textContent = coordinateLabels[method];
  }

  methodButtons.forEach(button => {
    button.addEventListener("click", () => selectMethod(button.dataset.method));
  });
  const initialMethod = methodButtons.find(button => button.getAttribute("aria-pressed") === "true") ||
    methodButtons[0];
  if (initialMethod) selectMethod(initialMethod.dataset.method);

  const links = Array.from(document.querySelectorAll('.contents a[href^="#"]:not(.back-top)'));
  function targetFor(hash) {
    try {
      return document.getElementById(decodeURIComponent(hash.slice(1)));
    } catch {
      return null;
    }
  }
  const targets = new Map(links.map(link => [link, targetFor(link.getAttribute("href"))]));
  const sections = Array.from(new Set(Array.from(targets.values()).filter(Boolean)))
    .sort((a, b) => a.compareDocumentPosition(b) & Node.DOCUMENT_POSITION_FOLLOWING ? -1 : 1);
  let currentSection;
  let updatePending = false;

  function markCurrent(section) {
    if (!section || section === currentSection) return;
    currentSection = section;
    links.forEach(link => {
      if (targets.get(link) === section) link.setAttribute("aria-current", "location");
      else link.removeAttribute("aria-current");
    });
  }

  function updateCurrent() {
    updatePending = false;
    if (!sections.length) return;
    const readingLine = Math.min(160, window.innerHeight * 0.2);
    let active = sections[0];
    for (const section of sections) {
      if (section.getBoundingClientRect().top <= readingLine) active = section;
      else break;
    }
    if (window.scrollY + window.innerHeight >= document.documentElement.scrollHeight - 2) {
      active = sections[sections.length - 1];
    }
    markCurrent(active);
  }

  function scheduleUpdate() {
    if (updatePending) return;
    updatePending = true;
    requestAnimationFrame(updateCurrent);
  }

  links.forEach(link => {
    link.addEventListener("click", event => {
      if (event.defaultPrevented || event.button !== 0 || event.metaKey ||
          event.ctrlKey || event.shiftKey || event.altKey) return;
      const menu = link.closest("details.mobile-contents");
      if (menu) menu.open = false;
      // Native anchors preserve deep links, browser history, and CSS scroll behavior.
    });
  });

  if (sections.length) {
    markCurrent(targetFor(window.location.hash) || sections[0]);
    if ("IntersectionObserver" in window) {
      const observer = new IntersectionObserver(scheduleUpdate, {
        rootMargin: "-10% 0px -65% 0px",
        threshold: [0, 1],
      });
      sections.forEach(section => observer.observe(section));
    }
    window.addEventListener("scroll", scheduleUpdate, { passive: true });
    window.addEventListener("resize", scheduleUpdate, { passive: true });
    window.addEventListener("hashchange", scheduleUpdate);
    window.addEventListener("pageshow", scheduleUpdate);
    window.addEventListener("load", scheduleUpdate, { once: true });
    scheduleUpdate();
  }
})();
