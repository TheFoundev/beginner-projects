# Instructions for Project 14: Create a Personal Link-in-Bio Page with Auto-Deploy

## Step-by-Step Guide

### 1. Create a GitHub Repository
- Go to [github.com](https://github.com) and create a free account.
- Create a new repository named `link-in-bio`.
- Initialize with a README.

### 2. Upload Your Files
```bash
git clone https://github.com/YOUR-USERNAME/link-in-bio.git
cd link-in-bio
# Copy index.html and .github/workflows/deploy.yml
git add .
git commit -m "Add link-in-bio page"
git push origin main
```

### 3. Enable GitHub Pages
- Go to your repo → **Settings** → **Pages** (left sidebar)
- Under **Source**, select `github-pages` branch.
- Click **Save**.

### 4. Watch Auto-Deploy
Every time you push changes to `main`:
1. GitHub Actions automatically picks up the change
2. It builds and deploys your site
3. Your live link updates within seconds!

### 5. View Your Live Site
- Your page is now live at `https://YOUR-USERNAME.github.io/link-in-bio/`

### 6. Customize
- Edit the links in `index.html` to point to your actual social profiles
- Change the name, bio, and colors to match your style
- Add/remove links as needed

---
*Your link-in-bio page is now live and automatically updates whenever you edit your code!*
