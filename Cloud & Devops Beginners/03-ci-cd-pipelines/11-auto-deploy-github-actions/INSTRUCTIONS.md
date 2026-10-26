# Instructions for Project 11: Auto-Deploy Your Website with GitHub Actions (CI/CD)

## Step-by-Step Guide

### 1. Create a GitHub Repository
- Go to [github.com](https://github.com) and create a free account.
- Create a new repository named `project-showcase`.
- Initialize with a README.

### 2. Add Your Website Code
On your local machine:
```bash
git clone https://github.com/YOUR-USERNAME/project-showcase.git
cd project-showcase
```
Copy `index.html` and the `.github/workflows/deploy.yml` file into your repo.

### 3. Commit and Push
```bash
git add .
git commit -m "Add project showcase website"
git push origin main
```

### 4. Enable GitHub Pages
- Go to your repository on GitHub → **Settings** → **Pages**
- Under **Source**, select the `github-pages` branch (auto-created by the workflow).
- Click **Save**.

### 5. Watch the Magic
Every time you push changes to `main`, GitHub Actions will:
1. **Build** — package your files
2. **Test** — verify they're valid
3. **Deploy** — update your live site

Check the **Actions** tab to see the pipeline run!

---
*Now your website deploys itself automatically every time you make a change!*
