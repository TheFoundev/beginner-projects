# Instructions for Project 5: Host a Static Website on AWS S3

## Step-by-Step Guide

### 1. Sign Up for AWS
- Go to [aws.amazon.com](https://aws.amazon.com) and create a free account.
- Use the **AWS Free Tier** — S3 includes 5GB of standard storage for 12 months.

### 2. Create an S3 Bucket
- Go to the **AWS Management Console** and open **S3**.
- Click **"Create bucket"**.
- Enter a **Bucket name** (must be unique, e.g., `my-resume-site-2026`).
- Choose a **Region** close to you.
- **Uncheck** "Block Public Access" (we need public access for hosting). Acknowledge the warning.
- Click **"Create bucket"**.

### 3. Upload Your Website Files
- Open your new bucket.
- Click the **"Upload"** button.
- Drag and drop `index.html` from this folder.
- Click **"Upload"** (wait for it to complete).

### 4. Enable Static Website Hosting
- In your bucket, go to the **"Properties"** tab.
- Scroll to **"Static website hosting"**.
- Select **"Use this bucket to host a website"**.
- Set **Index document** to `index.html`.
- Click **"Save changes"**.

### 5. Make Files Public
- Go to the **"Permissions"** tab.
- Under **Bucket Policy**, paste this policy (replace `your-bucket-name`):
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "PublicReadGetObject",
      "Effect": "Allow",
      "Principal": "*",
      "Action": "s3:GetObject",
      "Resource": "arn:aws:s3:::your-bucket-name/*"
    }
  ]
}
```
- Click **"Save changes"**.

### 6. Visit Your Website
- Go back to the **Properties** tab → **Static website hosting**.
- Copy the **Endpoint** URL — that's your live website!

---
*Your site is now hosted on AWS S3 with a global, redundant storage backend.*
