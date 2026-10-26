# Project 1: Deploy Your Personal HTML Resume to GitHub Pages

## Overview

A responsive, dark-mode-ready HTML resume with animations and a theme toggle — deployed for free on GitHub Pages.

## Files

| File | Description |
|------|-------------|
| `index.html` | Resume structure with semantic HTML |
| `style.css` | Full CSS styling with CSS variables & animations |
| `script.js` | Theme toggle, scroll animations, smooth scrolling |
| `INSTRUCTIONS.md` | Step-by-step deployment guide |

## Key Features

1. **Dark/Light Mode Toggle** — Click the moon/sun icon to switch themes. Preference is saved in `localStorage`.
2. **Scroll Animations** — Sections fade in as you scroll (Intersection Observer API).
3. **Responsive Design** — Adapts to mobile, tablet, and desktop screens.
4. **Semantic HTML** — Proper `<section>`, `<header>`, and `<footer>` tags for accessibility.

## Deployment

```bash
git clone https://github.com/YOUR-USERNAME/my-resume.git
cd my-resume
# Copy index.html, style.css, script.js here
git add .
git commit -m "Add resume website"
git push origin main

# Then: GitHub repo → Settings → Pages → Choose main branch → Save
# Visit: https://YOUR-USERNAME.github.io/my-resume/
```
