/* Wanisite — scène 3D du sourcing : usine → contrôle → envoi → chez vous.
   Three.js en temps réel, rendu « maquette » clair : matériaux mats, arêtes fines, lumière de jour.
   Pause hors écran, onglet caché ou mouvement réduit demandé. */
import * as THREE from '../vendor/three.module.min.js';

const stage = document.getElementById('scene3d');
if (stage) monter(stage);

function monter(stage) {
  let renderer;
  try { renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true, powerPreference: 'high-performance' }); }
  catch (e) { stage.classList.add('sans3d'); return; }
  if (!renderer.getContext()) { stage.classList.add('sans3d'); return; }

  const petit = matchMedia('(max-width: 760px)');
  const reduit = matchMedia('(prefers-reduced-motion: reduce)');
  const leger = petit.matches || (navigator.hardwareConcurrency || 8) <= 4;
  renderer.setPixelRatio(Math.min(devicePixelRatio || 1, leger ? 1.75 : 2));
  renderer.outputColorSpace = THREE.SRGBColorSpace;
  renderer.toneMapping = THREE.ACESFilmicToneMapping;
  renderer.toneMappingExposure = 1.05;
  renderer.shadowMap.enabled = true;
  renderer.shadowMap.type = THREE.PCFSoftShadowMap;
  stage.prepend(renderer.domElement);
  renderer.domElement.setAttribute('aria-hidden', 'true');

  const scene = new THREE.Scene();
  const camera = new THREE.OrthographicCamera(-1, 1, 1, -1, 0.1, 300);
  camera.position.set(40, 40, 40);
  camera.lookAt(0, 0, 0);

  /* ---------- couleurs : sable clair, blanc cassé, turquoise Wanisite, kraft ---------- */
  const C = {
    dalle: 0xf1ede6, dalleCote: 0xc9c1b4, beton: 0xdcd6cc, blanc: 0xf8f6f2, gris: 0xb8c2c8, ardoise: 0x3d4a5c,
    turquoise: 0x00c9c9, turquoiseFonce: 0x0a8f8f, kraft: 0xc99a62, eau: 0x3f9fd0, eauFonce: 0x2a7fb0,
    orange: 0xff8a3d, vert: 0x5fbf8f, bois: 0x9a6b45, coque: 0x1f3550, rouge: 0xe2574c,
  };
  const mat = (c, o = {}) => new THREE.MeshStandardMaterial({ color: c, roughness: 0.85, metalness: 0.02, flatShading: true, ...o });
  const M = {
    dalle: mat(C.dalle), dalleCote: mat(C.dalleCote), beton: mat(C.beton), blanc: mat(C.blanc, { roughness: 0.7 }),
    gris: mat(C.gris), ardoise: mat(C.ardoise), turquoise: mat(C.turquoise, { roughness: 0.55 }),
    turquoiseFonce: mat(C.turquoiseFonce, { roughness: 0.6 }), kraft: mat(C.kraft, { roughness: 0.95 }),
    eau: mat(C.eau, { roughness: 0.25, metalness: 0.1 }), orange: mat(C.orange, { roughness: 0.6 }), vert: mat(C.vert),
    bois: mat(C.bois), coque: mat(C.coque, { roughness: 0.6 }), rouge: mat(C.rouge),
    vitre: mat(0xbff3f3, { roughness: 0.2, emissive: 0x00c9c9, emissiveIntensity: 0.25 }),
    fumee: mat(0xffffff, { roughness: 1, transparent: true, opacity: 0.92 }),
    lumiere: new THREE.MeshBasicMaterial({ color: 0x9ff7f7 }),
  };
  const areteMat = new THREE.LineBasicMaterial({ color: 0x2b3a4a, transparent: true, opacity: 0.28 });

  function cube(l, h, p, m, x = 0, y = 0, z = 0, aretes = true) {
    const g = new THREE.BoxGeometry(l, h, p);
    const o = new THREE.Mesh(g, m);
    o.position.set(x, y + h / 2, z);
    o.castShadow = o.receiveShadow = true;
    if (aretes) o.add(new THREE.LineSegments(new THREE.EdgesGeometry(g), areteMat));
    return o;
  }
  function cyl(rh, rb, h, m, x = 0, y = 0, z = 0, seg = 14) {
    const o = new THREE.Mesh(new THREE.CylinderGeometry(rh, rb, h, seg), m);
    o.position.set(x, y + h / 2, z);
    o.castShadow = o.receiveShadow = true;
    return o;
  }
  function prisme(points, profondeur, m, x, y, z) {
    const forme = new THREE.Shape(points.map(([a, b]) => new THREE.Vector2(a, b)));
    const g = new THREE.ExtrudeGeometry(forme, { depth: profondeur, bevelEnabled: false });
    const o = new THREE.Mesh(g, m);
    o.position.set(x, y, z);
    o.castShadow = o.receiveShadow = true;
    o.add(new THREE.LineSegments(new THREE.EdgesGeometry(g), areteMat));
    return o;
  }
  function colis(s) {
    const g = new THREE.Group();
    g.add(cube(s, s * 0.78, s, M.kraft, 0, 0, 0));
    const scotch = cube(s * 1.02, s * 0.79, s * 0.18, M.turquoise, 0, 0, 0, false);
    g.add(scotch);
    return g;
  }
  function dalle(l, p, x, z) {
    const g = new THREE.Group();
    g.add(cube(l, 0.55, p, M.dalleCote, 0, -0.62, 0));
    g.add(cube(l - 0.08, 0.08, p - 0.08, M.dalle, 0, -0.08, 0));
    g.position.set(x, 0, z);
    return g;
  }

  /* ---------- lumière de jour ---------- */
  scene.add(new THREE.HemisphereLight(0xffffff, 0x8fa3b5, 1.45));
  const soleil = new THREE.DirectionalLight(0xfff4e6, 2.4);
  soleil.position.set(14, 26, 8);
  soleil.castShadow = true;
  soleil.shadow.mapSize.set(leger ? 1024 : 2048, leger ? 1024 : 2048);
  Object.assign(soleil.shadow.camera, { left: -26, right: 26, top: 26, bottom: -26, near: 1, far: 80 });
  soleil.shadow.bias = -0.0006;
  soleil.shadow.normalBias = 0.02;
  scene.add(soleil);

  const monde = new THREE.Group();
  scene.add(monde);

  /* ---------- 1. l'usine ---------- */
  const usine = new THREE.Group();
  usine.add(dalle(5.4, 5.4, 0, 0));
  usine.add(cube(3.2, 1.5, 2.6, M.blanc, -0.4, 0, -0.5));
  usine.add(cube(3.26, 0.22, 2.66, M.gris, -0.4, 0, -0.5, false));
  for (let i = 0; i < 3; i++) { // toits en dents de scie, verrières vers la caméra
    const t = prisme([[0, 0], [0.86, 0], [0.86, 0.72]], 2.6, M.turquoise, -2.0 + i * 1.07, 1.5, -1.8);
    usine.add(t);
    const verre = cube(0.04, 0.62, 2.5, M.vitre, -2.0 + i * 1.07 + 0.88, 1.5, -0.5, false);
    usine.add(verre);
  }
  for (let i = 0; i < 4; i++) usine.add(cube(0.42, 0.42, 0.04, M.vitre, -1.6 + i * 0.75, 0.6, 0.81, false));
  usine.add(cube(0.8, 0.9, 0.05, M.ardoise, 1.0, 0, 0.12, false)); // porte du quai, côté route
  usine.add(cyl(0.24, 0.3, 3.5, M.blanc, -1.6, 0, -1.55));
  usine.add(cyl(0.255, 0.255, 0.18, M.turquoise, -1.6, 2.6, -1.55));
  usine.add(cyl(0.255, 0.255, 0.18, M.turquoise, -1.6, 3.0, -1.55));
  const fumees = [];
  for (let k = 0; k < 7; k++) {
    const f = new THREE.Mesh(new THREE.IcosahedronGeometry(1, 1), M.fumee);
    f.castShadow = true; f.userData.decal = k / 7;
    usine.add(f); fumees.push(f);
  }
  // tapis roulant sous l'auvent
  usine.add(cube(1.6, 0.08, 0.5, M.ardoise, 1.95, 0.4, 0.12));
  for (const x of [1.3, 2.6]) usine.add(cube(0.08, 0.4, 0.42, M.gris, x, 0, 0.12));
  const tapis = [];
  for (let k = 0; k < 3; k++) { const c = colis(0.34); c.userData.decal = k / 3; usine.add(c); tapis.push(c); }
  const arbre = (x, z, s = 1) => { const a = new THREE.Group(); a.add(cyl(0.07 * s, 0.09 * s, 0.4 * s, M.bois, 0, 0, 0, 6)); const h = new THREE.Mesh(new THREE.IcosahedronGeometry(0.42 * s, 0), M.vert); h.position.y = 0.72 * s; h.castShadow = true; a.add(h); a.position.set(x, 0, z); return a; };
  usine.add(arbre(-2.1, 1.7), arbre(-1.3, 2.1, 0.8));
  for (let k = 0; k < 3; k++) { const c = colis(0.4); c.position.set(-0.3 + (k % 2) * 0.45, (k > 1 ? 0.32 : 0), 1.55); usine.add(c); }
  monde.add(usine);

  /* ---------- 2. le contrôle ---------- */
  const controle = new THREE.Group();
  controle.add(dalle(4.6, 4.6, 0, 0));
  controle.add(cube(2.2, 1.1, 1.8, M.blanc, -0.6, 0, -1.0));
  controle.add(prisme([[0, 0], [2.3, 0], [1.15, 0.5]], 1.9, M.turquoiseFonce, -1.75, 1.1, -1.95));
  controle.add(cube(0.6, 0.7, 0.05, M.ardoise, -0.2, 0, -0.08, false));
  // portique de contrôle au-dessus de la route
  const portique = new THREE.Group();
  portique.add(cube(0.16, 1.4, 0.16, M.gris, 0, 0, -0.7), cube(0.16, 1.4, 0.16, M.gris, 0, 0, 0.7));
  const poutre = cube(0.24, 0.22, 1.6, M.ardoise, 0, 1.4, 0);
  portique.add(poutre);
  const faisceau = new THREE.Mesh(new THREE.BoxGeometry(0.05, 1.25, 1.3), new THREE.MeshBasicMaterial({ color: 0x00e0e0, transparent: true, opacity: 0 }));
  faisceau.position.set(0, 0.75, 0);
  portique.add(faisceau);
  const valide = new THREE.Group(); // pastille ✓ qui apparaît au passage d'un colis
  const disque = new THREE.Mesh(new THREE.CylinderGeometry(0.34, 0.34, 0.08, 24), M.turquoise);
  disque.rotation.z = Math.PI / 2;
  const t1 = new THREE.Mesh(new THREE.BoxGeometry(0.1, 0.06, 0.18), M.blanc); t1.position.set(0.06, -0.05, -0.08); t1.rotation.x = -0.8;
  const t2 = new THREE.Mesh(new THREE.BoxGeometry(0.1, 0.06, 0.38), M.blanc); t2.position.set(0.06, 0.04, 0.08); t2.rotation.x = 0.85;
  valide.add(disque, t1, t2);
  valide.rotation.y = Math.PI / 4;
  valide.position.set(0, 2.15, 0);
  valide.scale.setScalar(0.001);
  portique.add(valide);
  portique.position.set(0.9, 0, 0.9);
  portique.rotation.y = Math.PI / 4;
  controle.add(portique);
  controle.add(arbre(1.5, -1.5, 0.9));
  monde.add(controle);

  /* ---------- 3. l'envoi : quai, grue, cargo ---------- */
  const envoi = new THREE.Group();
  envoi.add(dalle(5.6, 5.0, 0, 0));
  const eau = cube(2.9, 0.06, 4.8, M.eau, 1.25, -0.16, 0, false);
  envoi.add(eau);
  envoi.add(cube(0.12, 0.25, 4.8, M.gris, -0.2, -0.2, 0, false));
  const cargo = new THREE.Group();
  cargo.add(prisme([[-1.2, 0], [1.0, 0], [1.35, 0.5], [-1.3, 0.5]], 0.9, M.coque, 0, 0, -0.45));
  cargo.add(cube(0.5, 0.6, 0.7, M.blanc, -0.95, 0.5, 0));
  const pileCont = [[C.turquoise, -0.35, 0.5, -0.2], [C.orange, -0.35, 0.5, 0.2], [C.turquoiseFonce, 0.35, 0.5, -0.2], [C.blanc, 0.35, 0.5, 0.2], [C.orange, -0.35, 0.86, -0.2], [C.turquoise, 0.35, 0.86, 0.2]];
  for (const [c, x, y, z] of pileCont) cargo.add(cube(0.66, 0.36, 0.38, mat(c, { roughness: 0.6 }), x, y, z));
  cargo.rotation.y = Math.PI / 2;
  cargo.position.set(1.3, -0.12, 0.2);
  envoi.add(cargo);
  const grue = new THREE.Group();
  grue.add(cube(0.5, 0.18, 0.5, M.ardoise, 0, 0, 0));
  grue.add(cube(0.16, 2.6, 0.16, M.orange, 0, 0.18, 0));
  const fleche = new THREE.Group();
  fleche.add(cube(2.4, 0.14, 0.14, M.orange, 0.8, 0, 0));
  fleche.add(cube(0.5, 0.3, 0.3, M.ardoise, -0.55, -0.08, 0));
  const cable = new THREE.Mesh(new THREE.CylinderGeometry(0.015, 0.015, 1, 4), M.ardoise);
  fleche.add(cable);
  const charge = cube(0.6, 0.34, 0.36, M.turquoise, 0, 0, 0);
  fleche.add(charge);
  fleche.position.y = 2.8;
  grue.add(fleche);
  grue.position.set(-0.9, 0, -1.2);
  envoi.add(grue);
  monde.add(envoi);

  /* ---------- 4. chez vous : boutique livrée ---------- */
  const maison = new THREE.Group();
  maison.add(dalle(4.6, 4.6, 0, 0));
  maison.add(cube(2.2, 1.3, 1.8, M.blanc, -0.3, 0, -0.7));
  maison.add(cube(2.3, 0.12, 1.9, M.ardoise, -0.3, 1.3, -0.7));
  for (let k = 0; k < 5; k++) { // store à rayures
    const b = cube(0.44, 0.05, 0.6, k % 2 ? M.blanc : M.turquoise, -1.18 + k * 0.44, 1.0, 0.42, false);
    b.rotation.x = 0.45; maison.add(b);
  }
  maison.add(cube(0.5, 0.8, 0.05, M.ardoise, 0.3, 0, 0.21, false));
  maison.add(cube(0.8, 0.5, 0.05, M.vitre, -0.75, 0.35, 0.21, false));
  for (const [s, x, y, z] of [[0.42, 1.1, 0, 0.9], [0.36, 1.55, 0, 0.6], [0.32, 1.25, 0.33, 0.85]]) { const c = colis(s); c.position.set(x, y, z); maison.add(c); }
  const repere = new THREE.Group();
  const cone = new THREE.Mesh(new THREE.ConeGeometry(0.26, 0.7, 16), M.turquoise); cone.rotation.x = Math.PI; cone.position.y = 0.35; cone.castShadow = true;
  const tete = new THREE.Mesh(new THREE.SphereGeometry(0.3, 18, 12), M.turquoise); tete.position.y = 0.8; tete.castShadow = true;
  const point = new THREE.Mesh(new THREE.SphereGeometry(0.11, 10, 8), M.blanc); point.position.set(0, 0.8, 0.24);
  repere.add(cone, tete, point);
  repere.position.set(1.3, 1.5, -1.2);
  maison.add(repere);
  const anneau = new THREE.Mesh(new THREE.RingGeometry(0.28, 0.36, 32), new THREE.MeshBasicMaterial({ color: C.turquoise, transparent: true, side: THREE.DoubleSide, depthWrite: false }));
  anneau.rotation.x = -Math.PI / 2; anneau.position.set(1.3, 0.02, -1.2);
  maison.add(anneau);
  maison.add(arbre(-1.6, 1.4), arbre(1.6, -0.2, 0.7));
  monde.add(maison);

  const stations = [usine, controle, envoi, maison];

  /* ---------- route, colis qui voyagent, avion, nuages ---------- */
  const routeMat = mat(C.turquoise, { roughness: 0.5 });
  const v = new THREE.Vector3(), tmp = new THREE.Vector3();
  let pPortique = 0.33;
  let route = null, courbe = null;
  const traits = [];
  for (let k = 0; k < 26; k++) { const d = new THREE.Mesh(new THREE.SphereGeometry(0.06, 8, 6), M.lumiere); d.userData.decal = k / 26; monde.add(d); traits.push(d); }
  const voyageurs = [];
  for (let k = 0; k < 5; k++) { const c = colis(0.36); c.userData.decal = k / 5; monde.add(c); voyageurs.push(c); }

  const avion = new THREE.Group();
  const fuselage = new THREE.Mesh(new THREE.CylinderGeometry(0.14, 0.1, 1.4, 10), M.blanc); fuselage.rotation.z = Math.PI / 2; fuselage.castShadow = true;
  const nez = new THREE.Mesh(new THREE.ConeGeometry(0.14, 0.32, 10), M.blanc); nez.rotation.z = -Math.PI / 2; nez.position.x = 0.86;
  const aile = cube(0.36, 0.04, 1.7, M.blanc, 0, -0.02, 0); aile.castShadow = true;
  const derive = cube(0.24, 0.36, 0.04, M.turquoise, -0.58, 0.02, 0, false);
  const empennage = cube(0.2, 0.03, 0.6, M.blanc, -0.6, 0.02, 0, false);
  avion.add(fuselage, nez, aile, derive, empennage);
  monde.add(avion);

  const nuages = [];
  for (let k = 0; k < 4; k++) {
    const n = new THREE.Group();
    for (const [x, y, z, r] of [[0, 0, 0, 0.55], [0.55, -0.08, 0.1, 0.4], [-0.5, -0.1, -0.05, 0.38], [0.15, 0.25, 0, 0.36]]) {
      const b = new THREE.Mesh(new THREE.IcosahedronGeometry(r, 1), M.fumee); b.position.set(x, y, z); b.castShadow = true; n.add(b);
    }
    n.userData.decal = k / 4; n.userData.h = 5.2 + (k % 2) * 0.9;
    monde.add(n); nuages.push(n);
  }

  /* ---------- étiquettes HTML ancrées sur les stations ---------- */
  const textes = [['01', 'L’usine', 'Prix négocié'], ['02', 'Le contrôle', 'Échantillon vérifié'], ['03', 'L’envoi', 'Vers la France'], ['04', 'Chez vous', 'Livré']];
  const etiquettes = textes.map(([n, t, s]) => {
    const e = document.createElement('div');
    e.className = 'etq3d';
    e.innerHTML = `<b>${n}</b><span>${t}</span><small>${s}</small>`;
    stage.appendChild(e);
    return e;
  });
  const ancresEtq = [[1.4, 3.0, -1.9], [-0.6, 2.4, -1.0], [-0.9, 3.6, -1.2], [-0.3, 2.3, -0.7]]; // au-dessus de chaque bâtiment, à côté de la cheminée

  /* ---------- placement : en ligne sur ordinateur, en colonne sur téléphone ---------- */
  // En vue isométrique, l'axe (1,0,-1) est horizontal à l'écran et l'axe (1,0,1) vertical.
  function placer() {
    const vertical = stage.clientWidth / stage.clientHeight < 0.95;
    const pas = vertical ? 5.3 : 4.9;
    const dir = vertical ? new THREE.Vector3(1, 0, 1).normalize() : new THREE.Vector3(1, 0, -1).normalize();
    stations.forEach((s, i) => {
      const p = dir.clone().multiplyScalar((i - 1.5) * pas * Math.SQRT2);
      s.position.set(p.x, 0, p.z);
      s.rotation.y = vertical ? -Math.PI / 2 : 0;
    });
    if (route) { monde.remove(route); route.geometry.dispose(); }
    // points de passage dans chaque station (repère local) : sortie du tapis, portique, quai, porte de la boutique
    const ancres = [[2.5, 0.06, 0.4], [0.9, 0.06, 0.9], [-0.6, 0.06, 1.6], [0.4, 0.06, 1.3]];
    const pts = stations.map((s, i) => { s.updateMatrixWorld(true); return s.localToWorld(new THREE.Vector3(...ancres[i])); });
    courbe = new THREE.CatmullRomCurve3(pts, false, 'catmullrom', 0.25);
    // position du portique sur le trajet, pour allumer le scanner au bon moment
    let mieux = 1e9;
    for (let k = 0; k <= 400; k++) { const d = courbe.getPointAt(k / 400, tmp).distanceTo(pts[1]); if (d < mieux) { mieux = d; pPortique = k / 400; } }
    route = new THREE.Mesh(new THREE.TubeGeometry(courbe, 200, 0.07, 6, false), routeMat);
    route.receiveShadow = true;
    monde.add(route);
    cadrer();
  }

  // cadrage : la scène entière tient dans le cadre, avec une marge
  const boite = new THREE.Box3();
  function cadrer() {
    const l = stage.clientWidth, h = stage.clientHeight;
    renderer.setSize(l, h, false);
    camera.updateMatrixWorld();
    // station par station (une seule boîte autour d'une ligne en diagonale serait bien trop grande) ;
    // l'avion et les nuages peuvent sortir du cadre
    const coins = [];
    for (const st of stations) {
      boite.setFromObject(st, true);
      for (const x of [boite.min.x, boite.max.x]) for (const y of [boite.min.y, boite.max.y + 1.6]) for (const z of [boite.min.z, boite.max.z]) coins.push(new THREE.Vector3(x, y, z).applyMatrix4(camera.matrixWorldInverse));
    }
    const xs = coins.map(c => c.x), ys = coins.map(c => c.y);
    const cx = (Math.min(...xs) + Math.max(...xs)) / 2, cy = (Math.min(...ys) + Math.max(...ys)) / 2;
    let w = (Math.max(...xs) - Math.min(...xs)) * 1.1, hh = (Math.max(...ys) - Math.min(...ys)) * 1.1;
    if (w / hh > l / h) hh = w * h / l; else w = hh * l / h;
    Object.assign(camera, { left: cx - w / 2, right: cx + w / 2, top: cy + hh / 2, bottom: cy - hh / 2 });
    camera.updateProjectionMatrix();
  }

  /* ---------- interaction : la maquette suit légèrement le pointeur ---------- */
  let cibleRot = 0, rot = 0;
  stage.addEventListener('pointermove', (e) => {
    const r = stage.getBoundingClientRect();
    cibleRot = ((e.clientX - r.left) / r.width - 0.5) * 0.12;
  });
  stage.addEventListener('pointerleave', () => { cibleRot = 0; });

  /* ---------- animation ---------- */
  const BOUCLE = 12; // secondes pour qu'un colis fasse le trajet complet
  function animer(t) {
    // fumée de la cheminée
    for (const f of fumees) {
      const p = (t * 0.22 + f.userData.decal) % 1;
      const r = 0.1 + 0.42 * Math.sin(Math.PI * Math.min(1, p * 1.05)) * (0.5 + 0.8 * p);
      f.position.set(-1.6 + 1.3 * p + 0.08 * Math.sin(t * 2 + f.userData.decal * 9), 3.7 + 2.0 * p, -1.55 + 0.4 * p);
      f.scale.setScalar(r);
      f.rotation.set(t * 0.3, t * 0.2 + f.userData.decal, 0);
    }
    // cartons sur le petit tapis
    for (const c of tapis) { const p = (t * 0.35 + c.userData.decal) % 1; c.position.set(1.2 + 1.5 * p, 0.48, 0.12); c.visible = p < 0.96; }
    // route : tirets lumineux et colis voyageurs
    if (courbe) {
      for (const d of traits) { courbe.getPointAt((t * 0.05 + d.userData.decal) % 1, v); d.position.set(v.x, v.y + 0.09, v.z); }
      let passage = 0;
      for (const c of voyageurs) {
        const p = (t / BOUCLE + c.userData.decal) % 1;
        courbe.getPointAt(p, v);
        courbe.getTangentAt(p, tmp);
        const saut = Math.abs(Math.sin(p * Math.PI * 14)) * 0.08;
        c.position.set(v.x, v.y + 0.1 + saut, v.z);
        c.rotation.y = Math.atan2(tmp.x, tmp.z);
        // au passage sous le portique, le scanner s'allume
        const d = Math.abs(p - pPortique);
        if (d < 0.025) passage = Math.max(passage, 1 - d / 0.025);
      }
      faisceau.material.opacity = 0.55 * passage;
      const cible = passage > 0.2 ? 1 : 0.001;
      valide.scale.setScalar(THREE.MathUtils.lerp(valide.scale.x, cible, 0.12));
      valide.rotation.y = Math.PI / 4 + t * 2;
    }
    // grue qui charge le cargo, cargo qui tangue
    fleche.rotation.y = Math.sin(t * 0.6) * 1.1;
    const desc = 0.8 + 0.5 * (0.5 + 0.5 * Math.sin(t * 1.2));
    cable.scale.y = desc; cable.position.set(1.8, -desc / 2, 0);
    charge.position.set(1.8, -desc - 0.34, 0);
    cargo.position.y = -0.12 + Math.sin(t * 1.6) * 0.04;
    cargo.rotation.z = Math.sin(t * 1.1) * 0.03;
    // repère qui rebondit et anneau qui s'élargit
    repere.position.y = 1.5 + Math.abs(Math.sin(t * 2.4)) * 0.35;
    repere.rotation.y = t * 1.2;
    const a = (t * 0.7) % 1;
    anneau.scale.setScalar(1 + a * 2.2);
    anneau.material.opacity = 0.9 * (1 - a);
    // avion en boucle au-dessus du trajet
    const ang = t * 0.35;
    const centre = stations[2].position;
    avion.position.set(centre.x + Math.cos(ang) * 6.5, 6.4 + Math.sin(t * 0.9) * 0.25, centre.z + Math.sin(ang) * 4.2);
    avion.rotation.set(0, -ang - Math.PI / 2, Math.sin(ang) * 0.12 - 0.15);
    // nuages qui dérivent
    const centre0 = stations[0].position, centre3 = stations[3].position;
    for (const n of nuages) {
      const p = (t * 0.018 + n.userData.decal) % 1;
      n.position.lerpVectors(centre0, centre3, p * 1.4 - 0.2);
      n.position.y = n.userData.h;
      n.position.x += n.userData.decal * 3 - 1.5; n.position.z -= n.userData.decal * 2 - 1;
    }
    // suivi du pointeur
    rot += (cibleRot - rot) * 0.06;
    monde.rotation.y = rot;
  }

  function etiqueter() {
    const l = stage.clientWidth, h = stage.clientHeight;
    stations.forEach((s, i) => {
      v.set(...ancresEtq[i]);
      s.localToWorld(v);
      v.project(camera);
      etiquettes[i].style.transform = `translate(${(v.x * 0.5 + 0.5) * l}px, ${(-v.y * 0.5 + 0.5) * h}px) translate(-50%, -100%)`;
    });
  }

  let visible = true, actif = true, horloge = new THREE.Clock(), temps = 0;
  const dessiner = () => { animer(temps); renderer.render(scene, camera); etiqueter(); };
  function boucle() {
    requestAnimationFrame(boucle);
    const pause = !visible || document.hidden || reduit.matches; // reste animée derrière l'écran de candidature (floutée)
    const dt = Math.min(horloge.getDelta(), 0.05);
    if (pause) return;
    temps += dt;
    dessiner();
  }
  new IntersectionObserver(([e]) => { visible = e.isIntersecting; }, { rootMargin: '100px' }).observe(stage);
  new ResizeObserver(() => { placer(); dessiner(); }).observe(stage);
  placer();
  temps = 2.2; // première image déjà animée (fumée, colis en route)
  dessiner();
  stage.classList.add('pret');
  boucle();
}
