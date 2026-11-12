# Tidewind Isle — Matteo Prado's interactive portfolio

A drivable 3D island built with Three.js and Blender. Drive the buggy around the island and stop at the billboards to learn about Matteo's education, work, skills and photography.

- `index.html` — the whole game (Three.js r160, loaded from jsDelivr)
- `assets/` — 3D models made in Blender, as compressed GLB (meshopt geometry, WebP textures)
- `tex/` — terrain and material textures
- `music/` — the island theme, music by Steven Ibrahim
- `portfolio/` — resume, certificates, headshot and behind-the-scenes images

It is a static site: no build step. Deployed on Vercel. Add `?debug` to the URL for a frame-rate and draw-call readout.
