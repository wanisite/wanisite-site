/* Icônes 3D animées des cartes « Ce qu'on propose » : chargées et lancées seulement quand la carte est visible, à l'arrêt si l'utilisateur préfère moins d'animations. */
(function () {
  var vids = [].slice.call(document.querySelectorAll('video.svc-ico'));
  if (!vids.length) return;
  var reduit = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  if (reduit || !('IntersectionObserver' in window)) return;          // l'image fixe (poster) reste affichée
  var io = new IntersectionObserver(function (es) {
    es.forEach(function (e) {
      var el = e.target;
      if (e.isIntersecting) {
        if (!el.getAttribute('src') && el.dataset.src) el.setAttribute('src', el.dataset.src);
        var p = el.play(); if (p && p.catch) p.catch(function () {});
      } else el.pause();
    });
  }, { rootMargin: '140px' });
  vids.forEach(function (v) { io.observe(v); });
})();
