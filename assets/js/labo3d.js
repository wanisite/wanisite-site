/* Wanisite — « le laboratoire digital » en 3D (Three.js, temps réel).
   Une paillasse : quatre fioles SITE / SHOP / CRM / ADS qui bouillonnent, un bras robot qui prélève une goutte
   de chacune et la verse dans le bécher « croissance » (qui monte), un écran où la courbe se dessine.
   Rendu clair façon maquette, comme la scène de la page Sourcing. Pause hors écran / onglet caché / mouvement réduit. */
import * as THREE from '../vendor/three.module.min.js';

const stage = document.getElementById('labo3d');
if (stage) monter(stage);

function monter(stage) {
  let renderer;
  try { renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true, powerPreference: 'high-performance' }); }
  catch (e) { stage.classList.add('sans3d'); return; }
  if (!renderer.getContext()) { stage.classList.add('sans3d'); return; }

  const reduit = matchMedia('(prefers-reduced-motion: reduce)');
  const leger = matchMedia('(max-width: 760px)').matches || (navigator.hardwareConcurrency || 8) <= 4;
  renderer.setPixelRatio(Math.min(devicePixelRatio || 1, leger ? 1.75 : 2));
  renderer.outputColorSpace = THREE.SRGBColorSpace;
  renderer.toneMapping = THREE.ACESFilmicToneMapping;
  renderer.shadowMap.enabled = true;
  renderer.shadowMap.type = THREE.PCFSoftShadowMap;
  stage.prepend(renderer.domElement);
  renderer.domElement.setAttribute('aria-hidden', 'true');

  const scene = new THREE.Scene();
  const camera = new THREE.OrthographicCamera(-1, 1, 1, -1, 0.1, 300);
  camera.position.set(40, 34, 40);
  camera.lookAt(0, 0.6, 0);

  const mat = (c, o = {}) => new THREE.MeshStandardMaterial({ color: c, roughness: 0.8, metalness: 0.02, flatShading: true, ...o });
  const M = {
    sol: mat(0xeef2f5), solCote: mat(0xc3ced6), mur: mat(0xfbfcfd), plinthe: mat(0xd9e1e6),
    meuble: mat(0xf4f7f9), plan: mat(0x2b3a4a, { roughness: 0.5 }), poignee: mat(0x9fb0bc, { metalness: 0.5, roughness: 0.4 }),
    turquoise: mat(0x00c9c9, { roughness: 0.5 }), gris: mat(0xb8c2c8), ardoise: mat(0x3d4a5c), blanc: mat(0xffffff, { roughness: 0.6 }),
    verre: new THREE.MeshStandardMaterial({ color: 0xe8fbff, roughness: 0.05, metalness: 0.1, transparent: true, opacity: 0.3, depthWrite: false }),
    fumee: mat(0xffffff, { roughness: 1, transparent: true, opacity: 0.85 }),
    plaque: mat(0x3d4a5c, { roughness: 0.4 }), resistance: mat(0xff6a3d, { emissive: 0xff4a1d, emissiveIntensity: 0.6 }),
  };
  const arete = new THREE.LineBasicMaterial({ color: 0x2b3a4a, transparent: true, opacity: 0.22 });

  function cube(l, h, p, m, x = 0, y = 0, z = 0, aretes = true) {
    const g = new THREE.BoxGeometry(l, h, p), o = new THREE.Mesh(g, m);
    o.position.set(x, y + h / 2, z); o.castShadow = o.receiveShadow = true;
    if (aretes) o.add(new THREE.LineSegments(new THREE.EdgesGeometry(g), arete));
    return o;
  }
  function cyl(rh, rb, h, m, x = 0, y = 0, z = 0, seg = 18) {
    const o = new THREE.Mesh(new THREE.CylinderGeometry(rh, rb, h, seg), m);
    o.position.set(x, y + h / 2, z); o.castShadow = o.receiveShadow = true; return o;
  }
  function texte(largeur, hauteur, dessin) {
    const c = document.createElement('canvas'); c.width = largeur; c.height = hauteur;
    const t = new THREE.CanvasTexture(c); t.colorSpace = THREE.SRGBColorSpace; t.anisotropy = 4;
    dessin(c.getContext('2d'), c); t.needsUpdate = true; t.userData.canvas = c; return t;
  }
  const police = (g, taille, poids = 800) => { g.font = `${poids} ${taille}px Outfit, system-ui, sans-serif`; };

  /* ---------- lumière ---------- */
  scene.add(new THREE.HemisphereLight(0xffffff, 0x9fb3c2, 1.5));
  const soleil = new THREE.DirectionalLight(0xfff6ea, 2.3);
  soleil.position.set(12, 22, 14); soleil.castShadow = true;
  soleil.shadow.mapSize.set(leger ? 1024 : 2048, leger ? 1024 : 2048);
  Object.assign(soleil.shadow.camera, { left: -10, right: 10, top: 10, bottom: -10, near: 1, far: 60 });
  soleil.shadow.bias = -0.0006; soleil.shadow.normalBias = 0.02;
  scene.add(soleil);

  const labo = new THREE.Group();
  scene.add(labo);

  /* ---------- la pièce : sol et deux murs ---------- */
  const SZ = -0.95; // centre du sol : la pièce s'arrête un peu devant la paillasse
  labo.add(cube(9, 0.5, 4.5, M.solCote, 0, -0.55, SZ));
  const solTex = texte(512, 512, (g) => {
    g.fillStyle = '#eef2f5'; g.fillRect(0, 0, 512, 512); g.strokeStyle = 'rgba(0,143,143,.18)'; g.lineWidth = 2;
    for (let k = 0; k <= 512; k += 64) { g.beginPath(); g.moveTo(k, 0); g.lineTo(k, 512); g.stroke(); g.beginPath(); g.moveTo(0, k); g.lineTo(512, k); g.stroke(); }
  });
  solTex.wrapS = solTex.wrapT = THREE.RepeatWrapping; solTex.repeat.set(4.5, 2.25);
  const sol = new THREE.Mesh(new THREE.PlaneGeometry(8.9, 4.4), new THREE.MeshStandardMaterial({ map: solTex, roughness: 0.9 }));
  sol.rotation.x = -Math.PI / 2; sol.position.set(0, -0.04, SZ); sol.receiveShadow = true; labo.add(sol);
  labo.add(cube(9, 3.4, 0.16, M.mur, 0, -0.05, -3.12));
  labo.add(cube(0.16, 3.4, 4.5, M.mur, -4.42, -0.05, SZ));
  labo.add(cube(9, 0.14, 0.04, M.plinthe, 0, 0, -3.02, false));

  // affiche « tableau périodique » avec l'élément Ws
  const affiche = texte(512, 384, (g) => {
    g.fillStyle = '#ffffff'; g.fillRect(0, 0, 512, 384);
    const cs = ['#d9f1ef', '#e6eef2', '#fde3d6', '#e7e2f6', '#dff3e6'];
    for (let r = 0; r < 5; r++) for (let c = 0; c < 9; c++) {
      if ((r === 0 && c > 0 && c < 8) || (r === 1 && c > 1 && c < 7)) continue;
      g.fillStyle = cs[(r + c) % cs.length]; g.fillRect(14 + c * 54, 40 + r * 64, 48, 58);
    }
    g.fillStyle = '#00a8a8'; g.fillRect(150, 34, 212, 150);
    g.fillStyle = '#ffffff'; police(g, 22, 700); g.fillText('26', 166, 66);
    police(g, 92, 900); g.fillText('Ws', 186, 150); police(g, 22, 700); g.fillText('Wanisite', 166, 176);
    g.fillStyle = '#0c2030'; police(g, 20, 800); g.fillText('TABLEAU DES SERVICES', 14, 26);
  });
  const poster = new THREE.Mesh(new THREE.PlaneGeometry(2.4, 1.8), new THREE.MeshStandardMaterial({ map: affiche, roughness: 0.9 }));
  poster.rotation.y = Math.PI / 2; poster.position.set(-4.33, 2.25, -1.25); labo.add(poster);

  // étagère et flacons sur le mur du fond
  labo.add(cube(4.2, 0.08, 0.5, M.meuble, -1.6, 2.35, -2.8));
  const couleursFlacons = [0x00c9c9, 0xff8a3d, 0x7b6ef6, 0x5fbf8f, 0x2f7fd0, 0x00c9c9, 0xe2574c];
  couleursFlacons.forEach((c, k) => {
    const x = -3.4 + k * 0.58, h = 0.32 + (k % 3) * 0.12;
    labo.add(cyl(0.13, 0.15, h, mat(c, { roughness: 0.4 }), x, 2.43, -2.78));
    labo.add(cyl(0.07, 0.07, 0.1, M.ardoise, x, 2.43 + h, -2.78));
  });

  /* ---------- la paillasse ---------- */
  const BZ = -1.45, BH = 1.0;
  labo.add(cube(8.0, BH - 0.08, 1.7, M.meuble, 0, 0, BZ));
  labo.add(cube(8.1, 0.1, 1.8, M.plan, 0, BH - 0.08, BZ));
  for (let k = 0; k < 6; k++) {
    const x = -3.35 + k * 1.34;
    labo.add(cube(1.26, BH - 0.24, 0.03, M.blanc, x, 0.08, BZ + 0.86));
    labo.add(cube(0.36, 0.05, 0.05, M.poignee, x, BH - 0.36, BZ + 0.9, false));
  }
  const Y = BH + 0.02; // dessus du plan

  /* ---------- quatre fioles Erlenmeyer étiquetées ---------- */
  function profilErlen(echelle = 1) {
    const p = [[0.001, 0], [0.34, 0], [0.36, 0.04], [0.12, 0.56], [0.1, 0.6], [0.1, 0.82], [0.13, 0.85], [0.13, 0.88]];
    return p.map(([r, h]) => new THREE.Vector2(r * echelle, h * echelle));
  }
  function etiquette(mot, couleur) {
    return texte(256, 128, (g) => {
      g.fillStyle = '#ffffff'; g.fillRect(0, 0, 256, 128);
      g.fillStyle = couleur; g.fillRect(0, 0, 256, 22);
      g.fillStyle = '#0c2030'; police(g, 64, 900); g.textAlign = 'center'; g.fillText(mot, 128, 98);
    });
  }
  const fioles = [];
  const services = [['SITE', 0x00c9c9, '#00a8a8'], ['SHOP', 0xff8a3d, '#ff8a3d'], ['CRM', 0x7b6ef6, '#7b6ef6'], ['ADS', 0x5fbf8f, '#3fa874']];
  services.forEach(([mot, c, css], i) => {
    const g = new THREE.Group();
    const verre = new THREE.Mesh(new THREE.LatheGeometry(profilErlen(), 28), M.verre); verre.renderOrder = 3;
    const liquideMat = new THREE.MeshStandardMaterial({ color: c, roughness: 0.3, transparent: true, opacity: 0.88, emissive: c, emissiveIntensity: 0.12 });
    const liquide = new THREE.Mesh(new THREE.LatheGeometry([new THREE.Vector2(0.001, 0.01), new THREE.Vector2(0.32, 0.01), new THREE.Vector2(0.33, 0.04), new THREE.Vector2(0.2, 0.32), new THREE.Vector2(0.001, 0.32)], 28), liquideMat);
    liquide.castShadow = true; liquide.renderOrder = 2;
    const bouchon = cyl(0.11, 0.1, 0.12, M.ardoise, 0, 0.86, 0);
    const eti = new THREE.Mesh(new THREE.PlaneGeometry(0.5, 0.25), new THREE.MeshStandardMaterial({ map: etiquette(mot, css), roughness: 0.8 }));
    eti.position.set(0.235, 0.17, 0.235); eti.rotation.set(0, Math.PI / 4, 0); eti.rotateX(-0.4); eti.renderOrder = 4;
    g.add(liquide, verre, bouchon, eti);
    const bulles = [];
    for (let k = 0; k < 5; k++) { const b = new THREE.Mesh(new THREE.SphereGeometry(0.035, 8, 6), new THREE.MeshBasicMaterial({ color: 0xffffff, transparent: true, opacity: 0.8 })); b.userData.d = Math.random(); b.renderOrder = 3; g.add(b); bulles.push(b); }
    g.position.set(-3.3 + i * 0.85, Y, BZ + 0.15);
    labo.add(g);
    fioles.push({ g, liquide, bulles, couleur: c });
  });

  /* ---------- plaque chauffante et bécher « croissance » ---------- */
  const BX = 1.15, BZB = BZ + 0.1;
  labo.add(cube(1.1, 0.16, 1.0, M.plaque, BX, Y, BZB));
  const anneauChauffe = new THREE.Mesh(new THREE.TorusGeometry(0.36, 0.035, 8, 32), M.resistance);
  anneauChauffe.rotation.x = -Math.PI / 2; anneauChauffe.position.set(BX, Y + 0.17, BZB); labo.add(anneauChauffe);
  labo.add(cube(0.18, 0.06, 0.06, M.turquoise, BX + 0.38, Y + 0.05, BZB + 0.5, false));
  const becher = new THREE.Group(); becher.position.set(BX, Y + 0.17, BZB); labo.add(becher);
  const verreB = new THREE.Mesh(new THREE.CylinderGeometry(0.5, 0.48, 1.05, 32, 1, true), M.verre); verreB.position.y = 0.525; verreB.renderOrder = 3;
  const fondB = new THREE.Mesh(new THREE.CylinderGeometry(0.48, 0.48, 0.03, 32), M.verre); fondB.renderOrder = 3;
  for (let k = 1; k <= 4; k++) { const g = cube(0.12, 0.012, 0.02, M.ardoise, 0.35, k * 0.2, 0.35, false); g.rotation.y = Math.PI / 4; becher.add(g); } // graduations
  const liquideB = new THREE.Mesh(new THREE.CylinderGeometry(0.46, 0.46, 1, 32), new THREE.MeshStandardMaterial({ color: 0x00c9c9, roughness: 0.25, transparent: true, opacity: 0.85, emissive: 0x00c9c9, emissiveIntensity: 0.2 }));
  liquideB.renderOrder = 2; liquideB.castShadow = true;
  const etiB = new THREE.Mesh(new THREE.PlaneGeometry(0.62, 0.24), new THREE.MeshStandardMaterial({ map: texte(320, 128, (g) => {
    g.fillStyle = '#0c2030'; g.fillRect(0, 0, 320, 128); g.fillStyle = '#5ff0f0'; police(g, 26, 700); g.fillText('VOTRE', 22, 44);
    g.fillStyle = '#ffffff'; police(g, 52, 900); g.fillText('croissance', 18, 102);
  }), roughness: 0.8 }));
  etiB.position.set(0.36, 0.68, 0.36); etiB.rotation.y = Math.PI / 4; etiB.renderOrder = 4;
  becher.add(liquideB, verreB, fondB, etiB);
  const bullesB = [], vapeur = [];
  for (let k = 0; k < 8; k++) { const b = new THREE.Mesh(new THREE.SphereGeometry(0.045, 8, 6), new THREE.MeshBasicMaterial({ color: 0xffffff, transparent: true, opacity: 0.85 })); b.userData.d = k / 8; b.userData.a = k * 2.4; b.renderOrder = 3; becher.add(b); bullesB.push(b); }
  for (let k = 0; k < 5; k++) { const v = new THREE.Mesh(new THREE.IcosahedronGeometry(1, 1), M.fumee); v.userData.d = k / 5; becher.add(v); vapeur.push(v); }
  const goutte = new THREE.Mesh(new THREE.SphereGeometry(0.07, 12, 10), new THREE.MeshStandardMaterial({ color: 0x00c9c9, roughness: 0.2 }));
  goutte.visible = false; labo.add(goutte);

  /* ---------- bras robot (pipette) ---------- */
  const bras = new THREE.Group(); bras.position.set(-0.55, Y, BZ - 0.55); labo.add(bras);
  bras.add(cyl(0.3, 0.36, 0.18, M.ardoise));
  const pivot = new THREE.Group(); pivot.position.y = 0.18; bras.add(pivot);
  pivot.add(cyl(0.14, 0.16, 0.5, M.blanc));
  const epaule = new THREE.Group(); epaule.position.y = 0.55; pivot.add(epaule);
  epaule.add(new THREE.Mesh(new THREE.SphereGeometry(0.15, 14, 10), M.turquoise));
  const segA = cube(0.13, 1.25, 0.13, M.blanc, 0, 0, 0); epaule.add(segA);
  const coude = new THREE.Group(); coude.position.y = 1.25; epaule.add(coude);
  coude.add(new THREE.Mesh(new THREE.SphereGeometry(0.12, 12, 10), M.turquoise));
  const segB = cube(0.11, 1.1, 0.11, M.blanc, 0, 0, 0); coude.add(segB);
  const poignet = new THREE.Group(); poignet.position.y = 1.1; coude.add(poignet);
  const pipette = cyl(0.03, 0.06, 0.38, M.gris, 0, -0.38, 0); poignet.add(pipette);
  const pointe = new THREE.Object3D(); pointe.position.y = -0.4; poignet.add(pointe);

  /* ---------- écran : la courbe se dessine ---------- */
  const ecranTex = texte(512, 320, () => {});
  const ecranCanvas = ecranTex.userData.canvas;
  function dessinerEcran(p) {
    const g = ecranCanvas.getContext('2d');
    g.fillStyle = '#0c2030'; g.fillRect(0, 0, 512, 320);
    g.strokeStyle = 'rgba(95,240,240,.12)'; g.lineWidth = 1;
    for (let k = 40; k < 512; k += 40) { g.beginPath(); g.moveTo(k, 50); g.lineTo(k, 300); g.stroke(); }
    for (let k = 60; k < 300; k += 40) { g.beginPath(); g.moveTo(20, k); g.lineTo(492, k); g.stroke(); }
    g.fillStyle = '#5ff0f0'; police(g, 22, 700); g.fillText('wanisite.lab · résultats', 22, 34);
    const pts = 24, n = Math.max(2, Math.floor(p * pts));
    g.strokeStyle = '#00e0e0'; g.lineWidth = 5; g.lineJoin = 'round'; g.beginPath();
    for (let k = 0; k < n; k++) { const x = 30 + k * (450 / (pts - 1)); const y = 280 - (k / (pts - 1)) ** 1.6 * 200 - Math.sin(k * 1.3) * 10; k ? g.lineTo(x, y) : g.moveTo(x, y); }
    g.stroke();
    for (let k = 0; k < 6; k++) { const h = 20 + 30 * k * Math.min(1, p * 1.4); g.fillStyle = 'rgba(0,201,201,.35)'; g.fillRect(40 + k * 72, 300 - h, 40, h); }
    ecranTex.needsUpdate = true;
  }
  const ecran = new THREE.Group(); ecran.position.set(2.75, Y, BZ - 0.35); ecran.rotation.y = -0.25; labo.add(ecran);
  ecran.add(cube(0.5, 0.06, 0.32, M.ardoise, 0, 0, 0), cube(0.08, 0.5, 0.08, M.ardoise, 0, 0.06, -0.05));
  ecran.add(cube(1.62, 1.02, 0.07, M.ardoise, 0, 0.5, -0.02));
  const dalleEcran = new THREE.Mesh(new THREE.PlaneGeometry(1.5, 0.92), new THREE.MeshBasicMaterial({ map: ecranTex })); dalleEcran.position.set(0, 1.01, 0.02); ecran.add(dalleEcran);
  ecran.add(cube(0.9, 0.04, 0.3, M.gris, -0.1, 0, 0.45)); // clavier

  /* ---------- portoir à tubes et microscope ---------- */
  const portoir = new THREE.Group(); portoir.position.set(2.2, Y, BZ + 0.5); labo.add(portoir);
  portoir.add(cube(1.0, 0.06, 0.26, M.blanc, 0, 0.0, 0), cube(1.0, 0.06, 0.26, M.blanc, 0, 0.32, 0));
  portoir.add(cube(0.04, 0.38, 0.22, M.blanc, -0.48, 0, 0), cube(0.04, 0.38, 0.22, M.blanc, 0.48, 0, 0));
  const tubes = [];
  [0x00c9c9, 0xff8a3d, 0x7b6ef6, 0x5fbf8f, 0x2f7fd0].forEach((c, k) => {
    const x = -0.36 + k * 0.18;
    const t = new THREE.Mesh(new THREE.CylinderGeometry(0.06, 0.06, 0.62, 14, 1, true), M.verre); t.position.set(x, 0.33, 0); t.renderOrder = 3; portoir.add(t);
    const l = new THREE.Mesh(new THREE.CylinderGeometry(0.052, 0.052, 1, 14), mat(c, { roughness: 0.3, emissive: c, emissiveIntensity: 0.15 })); l.renderOrder = 2; portoir.add(l);
    tubes.push({ l, x, d: k * 0.7 });
  });
  const micro = new THREE.Group(); micro.position.set(3.45, Y, BZ + 0.35); micro.rotation.y = -0.6; labo.add(micro);
  micro.add(cube(0.5, 0.08, 0.6, M.ardoise, 0, 0, 0), cube(0.1, 0.8, 0.12, M.blanc, 0, 0.08, -0.2));
  const tete = cube(0.14, 0.5, 0.14, M.blanc, 0, 0, 0); tete.rotation.x = 0.5; tete.position.set(0, 0.86, -0.06); micro.add(tete);
  micro.add(cube(0.36, 0.04, 0.3, M.gris, 0, 0.36, 0.02), cyl(0.05, 0.05, 0.2, M.turquoise, 0, 0.42, 0.05));

  /* ---------- plante (la touche de vie) ---------- */
  labo.add(cyl(0.22, 0.17, 0.4, M.blanc, -3.9, -0.04, 0.7));
  for (let k = 0; k < 5; k++) { const f = new THREE.Mesh(new THREE.IcosahedronGeometry(0.26, 0), mat(0x5fbf8f)); f.position.set(-3.9 + Math.cos(k) * 0.18, 0.5 + k * 0.12, 0.7 + Math.sin(k) * 0.18); f.castShadow = true; labo.add(f); }

  /* ---------- cadrage ---------- */
  const boite = new THREE.Box3();
  function cadrer() {
    const l = stage.clientWidth, h = stage.clientHeight;
    if (!l || !h) return;
    renderer.setSize(l, h, false);
    camera.updateMatrixWorld();
    boite.setFromObject(labo, true);
    const coins = [];
    for (const x of [boite.min.x, boite.max.x]) for (const y of [boite.min.y, boite.max.y]) for (const z of [boite.min.z, boite.max.z]) coins.push(new THREE.Vector3(x, y, z).applyMatrix4(camera.matrixWorldInverse));
    const xs = coins.map((c) => c.x), ys = coins.map((c) => c.y);
    const cx = (Math.min(...xs) + Math.max(...xs)) / 2, cy = (Math.min(...ys) + Math.max(...ys)) / 2;
    let w = (Math.max(...xs) - Math.min(...xs)) * 1.03, hh = (Math.max(...ys) - Math.min(...ys)) * 1.03;
    if (w / hh > l / h) hh = w * h / l; else w = hh * l / h;
    Object.assign(camera, { left: cx - w / 2, right: cx + w / 2, top: cy + hh / 2, bottom: cy - hh / 2 });
    camera.updateProjectionMatrix();
  }

  /* ---------- animation ---------- */
  const CYCLE = 10; // secondes : le bras passe par les 4 fioles puis verse dans le bécher
  const v = new THREE.Vector3(), cible = new THREE.Vector3(), local = new THREE.Vector3();
  const lerp = THREE.MathUtils.lerp, ease = (x) => x < 0.5 ? 2 * x * x : 1 - (-2 * x + 2) ** 2 / 2;
  // positions cibles du bout de pipette (repère du labo) : au-dessus de chaque fiole, puis du bécher
  const arrets = [...fioles.map((f) => f.g.position.clone().add(new THREE.Vector3(0, 1.05, 0))), new THREE.Vector3(BX, Y + 1.55, BZB)];
  // cinématique simple : le pivot tourne vers la cible, l'épaule et le coude se plient pour atteindre la distance
  function viser(p) {
    local.copy(p).sub(bras.position); local.y -= 0.18 + 0.55;
    const yaw = Math.atan2(local.x, local.z);
    pivot.rotation.y = yaw;
    const d = Math.min(2.3, Math.hypot(local.x, local.z)), hgt = local.y + 0.4;
    const L1 = 1.25, L2 = 1.1, r = Math.min(L1 + L2 - 0.01, Math.hypot(d, hgt));
    const a2 = Math.acos(THREE.MathUtils.clamp((L1 * L1 + L2 * L2 - r * r) / (2 * L1 * L2), -1, 1));
    const a1 = Math.atan2(d, hgt) - Math.asin(THREE.MathUtils.clamp(L2 * Math.sin(a2) / r, -1, 1));
    epaule.rotation.x = a1; coude.rotation.x = Math.PI - a2; poignet.rotation.x = -(a1 + coude.rotation.x) + Math.PI;
  }

  function animer(t) {
    // bulles dans les fioles, petit remous de surface
    fioles.forEach((f, i) => {
      for (const b of f.bulles) { const p = (t * 0.6 + b.userData.d + i * 0.17) % 1; b.position.set(Math.sin(b.userData.d * 30 + t) * 0.12, 0.04 + p * 0.3, Math.cos(b.userData.d * 20) * 0.12); b.scale.setScalar(0.6 + p * 0.8); }
      f.liquide.scale.y = 1 + Math.sin(t * 3 + i) * 0.03;
    });
    // cycle du bras : 4 prélèvements puis le versement
    const c = (t % CYCLE) / CYCLE, etape = Math.min(4, Math.floor(c * 5)), loc = (c * 5) % 1;
    const de = arrets[(etape + 4) % 5], vers = arrets[etape];
    const m = ease(Math.min(1, loc / 0.55));
    cible.lerpVectors(de, vers, m);
    const plonge = loc > 0.55 && loc < 0.9 ? Math.sin((loc - 0.55) / 0.35 * Math.PI) * (etape < 4 ? 0.32 : 0.05) : 0;
    cible.y -= plonge;
    viser(cible);
    // la goutte tombe dans le bécher pendant le versement
    if (etape === 4 && loc > 0.6) {
      const k = (loc - 0.6) / 0.4;
      pointe.getWorldPosition(v); goutte.visible = true;
      goutte.position.set(BX, lerp(v.y, Y + 0.3 + niveau(t), k), BZB);
    } else goutte.visible = false;
    // le bécher se remplit sur plusieurs cycles, puis repart
    const n = niveau(t);
    liquideB.scale.y = n; liquideB.position.y = 0.03 + n / 2;
    for (const b of bullesB) { const p = (t * 0.7 + b.userData.d) % 1; b.position.set(Math.cos(b.userData.a) * 0.28, 0.06 + p * n, Math.sin(b.userData.a) * 0.28); b.visible = p * n < n - 0.02; }
    for (const s of vapeur) { const p = (t * 0.25 + s.userData.d) % 1; s.position.set(Math.sin(t + s.userData.d * 9) * 0.12, 1.1 + p * 1.2, Math.cos(t * 0.7 + s.userData.d * 9) * 0.1); s.scale.setScalar(0.06 + 0.14 * Math.sin(Math.PI * p)); }
    anneauChauffe.material.emissiveIntensity = 0.5 + 0.3 * Math.sin(t * 2.2);
    // tubes qui se remplissent et se vident doucement
    for (const tb of tubes) { const h = 0.18 + 0.32 * (0.5 + 0.5 * Math.sin(t * 0.9 + tb.d)); tb.l.scale.y = h; tb.l.position.set(tb.x, 0.06 + h / 2, 0); }
    // écran
    if (Math.floor(t * 12) !== animer.dernier) { animer.dernier = Math.floor(t * 12); dessinerEcran(((t % (CYCLE * 3)) / (CYCLE * 3))); }
    // la maquette suit légèrement le pointeur
    rot += (cibleRot - rot) * 0.06; labo.rotation.y = rot;
  }
  const niveau = (t) => 0.18 + 0.72 * ((t % (CYCLE * 3)) / (CYCLE * 3));

  let cibleRot = 0, rot = 0;
  stage.addEventListener('pointermove', (e) => { const r = stage.getBoundingClientRect(); cibleRot = ((e.clientX - r.left) / r.width - 0.5) * 0.14; });
  stage.addEventListener('pointerleave', () => { cibleRot = 0; });

  let visible = true, temps = 4.2;
  const horloge = new THREE.Clock();
  const dessiner = () => { animer(temps); renderer.render(scene, camera); };
  (function boucle() {
    requestAnimationFrame(boucle);
    const dt = Math.min(horloge.getDelta(), 0.05);
    if (!visible || document.hidden || reduit.matches) return;
    temps += dt; dessiner();
  })();
  new IntersectionObserver(([e]) => { visible = e.isIntersecting; }, { rootMargin: '100px' }).observe(stage);
  new ResizeObserver(() => { cadrer(); dessiner(); }).observe(stage);
  cadrer(); dessiner();
  stage.classList.add('pret');
}
