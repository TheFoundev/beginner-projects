# Instructions for Project 2: Host a Personal Portfolio Site on Netlify

## Overview

A modern, responsive portfolio website with skill bars, project cards, and a contact form — deployed instantly on Netlify.

## Files

| File | Description |
|------|-------------|
| `index.html` | Full portfolio page (hero, projects, skills, contact) |
| `style.css` | Responsive CSS with CSS variables and animations |
| `script.js` | Mobile nav, smooth scroll, skill animation, form handling |
| `netlify.toml` | Netlify deployment config with redirects & headers |
| `INSTRUCTIONS.md` | Step-by-step deployment guide |

## Quick Deploy Options

### Option 1: Drag & Drop (Easiest)
1. Zip the project folder
2. Go to [https://app.netlify.com/drop](https://app.netlify.com/drop)
3. Drag the zip file into the browser

### Option 2: Git Integration (Recommended)
```bash
git init
git add .
git commit -m "Add portfolio"
git branch -M main
git remote add origin https://github.com/YOUR-USERNAME/portfolio.git
git push -u origin main

# Then: Connect repo on https://app.netlify.com → New site → Import
```

## Key Features

- **Animated skill bars** — Fill on scroll
- **Project cards** — With hover effects and tech tags
- **Contact form** — Client-side validation
- **Mobile-responsive** — Hamburger menu & adaptive layout
