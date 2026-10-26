# Instructions for Project 19: Create a No-Code Contact Form with Formspree

## Step-by-Step Guide

### 1. Sign Up for Formspree
- Go to [https://formspree.io](https://formspree.io) and create a free account.
- The free plan includes 50 submissions per month.

### 2. Create a New Form
- Log in to your Formspree dashboard.
- Click **"New Form"**.
- Give it a name (e.g., "Website Contact Form").
- Click **"Create"**.

### 3. Get Your Form Endpoint
- Your dashboard will show an endpoint URL like:
  ```
  https://formspree.io/f/abc123xy
  ```
- Copy this URL.

### 4. Update Your HTML
Open `index.html` and replace `YOUR_FORM_ID` (in the form action) with your Formspree form ID:
```html
<form action="https://formspree.io/f/abc123xy" method="POST">
```

### 5. Deploy Your Website
- Push your `index.html` to a GitHub repo and deploy with GitHub Pages, Netlify, or Vercel.
- Or simply open `index.html` in your browser for a quick test (note: the form submission will work, but you need to be online).

### 6. Test
- Visit your live page.
- Fill out the form and submit.
- Check your email — you should receive the message!

---
*No backend code, no servers, no databases — Formspree handles everything for you!*
