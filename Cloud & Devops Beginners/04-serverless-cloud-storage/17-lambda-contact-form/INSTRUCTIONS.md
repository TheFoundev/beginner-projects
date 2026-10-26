# Instructions for Project 17: Create a Serverless Contact Form Handler with AWS Lambda

## Step-by-Step Guide

### 1. Sign Up for AWS
- Go to [aws.amazon.com](https://aws.amazon.com) and create a free account.
- AWS Lambda has 1 million free requests per month.

### 2. Verify Your Email with SES
- Go to the [SES Console](https://console.aws.amazon.com/ses)
- Click **"Verified identities"** → **"Create identity"** → **Email**
- Enter your email and verify it (check your inbox for the confirmation link).

### 3. Create the Lambda Function
- Go to the [AWS Lambda Console](https://console.aws.amazon.com/lambda)
- Click **"Create function"** → **Author from scratch**
  - **Function name**: `contact-form-handler`
  - **Runtime**: Python 3.11
- Click **"Create function"**

### 4. Add Your Code
- Replace the default code with the content of `lambda_function.py`.
- Set environment variables:
  - `SENDER_EMAIL` = your verified email
  - `RECIPIENT_EMAIL` = the email that should receive messages

### 5. Add an API Gateway Trigger
- Under **"Function URL"** or **"API Gateway"**, add an HTTP trigger.
- Create a new HTTP API.
- Set **Security** to "Open".
- Note the **Invoke URL** — this is your API endpoint.

### 6. Update Your Website
- Replace `YOUR_FORM_ID` in `index.html` with your Lambda's API endpoint URL.

### 7. Test
- Host the `index.html` on GitHub Pages or Netlify (see Project 1).
- Submit the form and check your email inbox.

---
*You now have a fully serverless contact form with no servers to manage!*
