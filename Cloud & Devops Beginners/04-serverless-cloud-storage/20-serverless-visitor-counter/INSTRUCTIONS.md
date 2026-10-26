# Instructions for Project 20: Deploy a Serverless "Visitor Counter" with Upstash & Vercel

## Step-by-Step Guide

### 1. Sign Up for Accounts
- [Vercel](https://vercel.com) (free) — for serverless functions & hosting
- [Upstash](https://upstash.com) (free tier) — for serverless Redis

### 2. Create a Redis Database on Upstash
- Go to [https://console.upstash.com](https://console.upstash.com) → **Redis** → **Create Database**
- Name it `visitor-counter`
- Choose your region (closest to your users).
- Click **Create**.

### 3. Get Your Redis Credentials
- After creation, click on your database.
- Copy the `REST URL` and `TOKEN`.
- (These look like `https://xxx.upstash.io` and `xxxxxx...`)

### 4. Create a Vercel Project
- Go to [https://vercel.com/new](https://vercel.com/new)
- Sign up with GitHub and import a new project.
- Create a new GitHub repo and push this code.
- Or use the Vercel CLI:
  ```bash
  npm install -g vercel
  vercel
  ```

### 5. Add Environment Variables on Vercel
In your Vercel project → **Settings** → **Environment Variables**:
| Name        | Value                        |
|-------------|------------------------------|
| `REDIS_URL`  | Your Upstash REST URL     |
| `REDIS_TOKEN`| Your Upstash token        |

### 6. Deploy
```bash
vercel --prod
```
Or push to GitHub and let Vercel auto-deploy.

### 7. See It Live
Visit your Vercel URL — each load increments the counter in Redis:
```
https://your-project.vercel.app
```

---
*You now have a full serverless stack: frontend + API + database, all auto-scaling and free!*
