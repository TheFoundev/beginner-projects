# Instructions for Project 18: Build a "Fortune Cookie" Serverless API with Netlify Functions

## Step-by-Step Guide

### 1. Sign Up for Netlify & GitHub
- [GitHub](https://github.com) (free account)
- [Netlify](https://netlify.com) (free account)

### 2. Create a GitHub Repository
- Go to GitHub → **New repository** → name it `fortune-cookie-api`

### 3. Upload Your Files
```bash
git clone https://github.com/YOUR-USERNAME/fortune-cookie-api.git
cd fortune-cookie-api
# Copy index.html and netlify/functions/fortune.js
git add .
git commit -m "Add fortune cookie API"
git push origin main
```

### 4. Deploy on Netlify
- Go to [https://app.netlify.com](https://app.netlify.com)
- Click **"Add new site"** → **"Import an existing project"**
- Connect your GitHub and select `fortune-cookie-api`
- Click **"Deploy site"**

### 5. Test Your API
- Visit your site at `https://fortune-cookie-api.netlify.app`
- Click "Get New Fortune" — the frontend calls `/api/fortune`,
  which triggers your serverless function in the cloud!

### 6. Test the API Directly
You can also visit the API endpoint directly:
```
https://fortune-cookie-api.netlify.app/.netlify/functions/fortune
```
(Netlify automatically creates a friendly `/api/fortune` URL for your function.)

---
*Your API is now live — anyone can call it to get a random fortune!*
