# Instructions for Project 16: Store and Display Photos on Cloud Storage (AWS S3)

## Step-by-Step Guide

### 1. Sign Up for AWS
- Go to [aws.amazon.com](https://aws.amazon.com) and create a free account.
- AWS Free Tier includes 5GB of S3 storage for 12 months.

### 2. Create a Bucket
- Go to the [AWS S3 Console](https://s3.console.aws.amazon.com/)
- Click **"Create bucket"**.
- **Bucket name**: `my-photo-gallery-2026` (must be unique)
- **Region**: Pick one near you.
- **Uncheck** "Block Public Access" and acknowledge the warning.
- Scroll down and click **"Create bucket"**.

### 3. Upload Your Photos
- Open your new bucket.
- Click **"Upload"** → **"Add files"**.
- Select your photos (or use placeholder links from the HTML).
- Click **"Upload"**.

### 4. Make Photos Publicly Accessible
The easiest way: install the AWS CLI and run:
```bash
aws s3 cp . s3://my-photo-gallery-2026/ --recursive --acl public-read
```

Or use the console:
- Select your uploaded files.
- **Actions** → **Set metadata** or use **Bucket Policy** (see INSTRUCTIONS.md for the policy).

### 5. Enable Static Website Hosting
- Bucket → **Properties** tab → **Static website hosting**
- Choose **"Use this bucket to host a website"**
- Set **Index document** to `index.html`
- Click **Save**

### 6. Add Your Bucket Policy
Go to **Permissions** → **Bucket Policy** and paste:
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": "*",
      "Action": "s3:GetObject",
      "Resource": "arn:aws:s3:::my-photo-gallery-2026/*"
    }
  ]
}
```

### 7. View Your Gallery
Use the bucket's **Static website endpoint URL** to view your live gallery!

---
*Your photos are now stored in the cloud's most durable storage and served to visitors worldwide.*
