# Instructions for Project 13: Auto-Build and Deploy a Docker Image with GitHub Actions

## Step-by-Step Guide

### 1. Sign Up for Docker Hub
- Go to [hub.docker.com](https://hub.docker.com) and create a free account.
- Get your **username** ready.

### 2. Create a Docker Hub Access Token
- Go to Docker Hub → **Account Settings** → **Security** → **New Access Token**.
- Name it `github-actions-token`.
- Copy the generated token.

### 3. Create a GitHub Repository
- Go to [github.com](https://github.com) and create a new repo named `todo-api-docker`.

### 4. Add Your Code to GitHub
```bash
git clone https://github.com/YOUR-USERNAME/todo-api-docker.git
cd todo-api-docker
# Copy app.py, Dockerfile, .dockerignore, and .github/workflows/docker-build.yml
git add .
git commit -m "Add todo API with Docker"
git push origin main
```

### 5. Configure GitHub Secrets
In your GitHub repo → **Settings** → **Secrets and variables** → **Actions**:
- Add `DOCKERHUB_USERNAME` = your Docker Hub username
- Add `DOCKERHUB_TOKEN` = the token you created in step 2

### 6. Update the Workflow File
Open `.github/workflows/docker-build.yml` and replace `yourusername/todo-api` with your actual Docker Hub username.

### 7. Watch the Pipeline
- Push any change to `main`.
- Go to the **Actions** tab — watch it build and push the Docker image automatically!
- Test it locally:
  ```bash
  docker pull YOUR_USERNAME/todo-api:latest
  docker run -p 5000:5000 YOUR_USERNAME/todo-api:latest
  ```

---
*Every commit now automatically builds and publishes a new container image to the cloud!*
