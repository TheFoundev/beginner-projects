# Instructions for Project 15: Automate Your Portfolio with Markdown to Web

## Step-by-Step Guide

### 1. Create a GitHub Repository
- Go to [github.com](https://github.com) and create a new repo named `markdown-blog`.

### 2. Add Your Files
```bash
git clone https://github.com/YOUR-USERNAME/markdown-blog.git
cd markdown-blog
# Copy README.md and .github/workflows/build-deploy.yml
git add .
git commit -m "Add markdown blog"
git push origin main
```

### 3. Enable GitHub Pages
- Go to your repo → **Settings** → **Pages**
- Source: `github-pages` branch
- Click **Save**

### 4. Watch the Magic
Every time you edit `README.md` and push:
1. GitHub Actions converts your Markdown to styled HTML
2. The new page deploys automatically to GitHub Pages

---
*Now you can write content in simple Markdown, and automation turns it into a polished website!*
