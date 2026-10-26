# Instructions for Project 4: Deploy a Simple Website with Vercel

## Step-by-Step Guide

### 1. Create a GitHub Repository
- Go to [github.com](https://github.com) and sign in or create a free account.
- Click **"New"** to create a new repository.
- Name it `fun-facts-site`.
- Choose **Public** and check **"Add a README file"**.
- Click **"Create repository"**.

### 2. Upload Your Files
- On your repository page, click **"Add file"** then **"Upload files"**.
- Drag and drop `index.html` from this folder into the upload area.
- Click **"Commit changes"**.

### 3. Deploy with Vercel
**Option A: Web Dashboard (Easiest)**
- Go to [https://vercel.com/new](https://vercel.com/new)
- Sign up with your GitHub account.
- Select your `fun-facts-site` repository.
- Click **"Deploy"** — done!

**Option B: Vercel CLI**
- Install the CLI: `npm install -g vercel`
- In your terminal, run: `vercel`
- Follow the prompts to deploy.

### 4. View Your Live Site
- Your site is now live at `https://fun-facts-site.vercel.app` (or similar).
- Every commit to `main` will trigger a new automatic deployment!

---
*Vercel provides a global CDN, automatic SSL, and instant cache invalidation for free.*
