# Instructions for Project 3: Create a Personal Website with Firebase Hosting

## Step-by-Step Guide

### 1. Install Firebase CLI
Open your terminal and run:
```bash
npm install -g firebase-tools
```

### 2. Log In to Firebase
```bash
firebase login
```
This opens a browser window — sign in with your Google account.

### 3. Initialize Your Project
Navigate to this folder in your terminal, then run:
```bash
firebase init hosting
```
- Select your Firebase project (or create a new one).
- Set `public` directory: type `.` (current folder).
- Configure as a single-page app: type `y`.
- File `index.html` exists: type `n` (we use our own).

### 4. Deploy to Firebase
```bash
firebase deploy
```
After deployment, you'll get a live URL like:
`https://your-project-id.web.app`

### 5. (Optional) Add a Custom Domain
- Go to the [Firebase Console](https://console.firebase.google.com/)
- Select your project → Hosting → Add custom domain.

---
*Your site is now live on Google's global CDN with SSL! 🚀*
