/* Aggregate visitor analytics, without click events. No passwords or API keys. */
(() => {
  "use strict";

  // Verified owner-controlled account; dashboard and visitor counter are private.
  const endpoint = "https://fmahdisoltani.goatcounter.com/count";
  if (!/^https:\/\/[a-z0-9-]+\.goatcounter\.com\/count$/.test(endpoint)) return;

  const paths = new Set([
    "/steerable-lens/",
    "/steerable-lens/index.html",
    "/steerable-lens/explore.html",
  ]);
  if (location.protocol !== "https:" ||
      location.hostname !== "fmahdisoltani.github.io" ||
      !paths.has(location.pathname)) return;

  // Respect browser privacy preferences and avoid duplicate initialization.
  if (navigator.globalPrivacyControl || navigator.doNotTrack === "1" ||
      window.doNotTrack === "1" || document.getElementById("site-analytics")) return;

  window.goatcounter = {
    path: location.pathname.replace(/\/index\.html$/, "/"),
    referrer: "",
    no_events: true,
  };
  const script = document.createElement("script");
  script.id = "site-analytics";
  script.async = true;
  script.src = "https://gc.zgo.at/count.js";
  script.referrerPolicy = "no-referrer";
  script.setAttribute("data-goatcounter", endpoint);
  document.head.appendChild(script);
})();
