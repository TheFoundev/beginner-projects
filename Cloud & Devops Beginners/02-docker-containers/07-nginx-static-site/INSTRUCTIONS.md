# Instructions for Project 7: Containerize a Static HTML Website with Nginx

## Step-by-Step Guide

### 1. Build the Docker Image
In your terminal, navigate to this folder and run:
```bash
docker build -t my-website .
```

### 2. Run the Container
```bash
docker run -d -p 8080:80 my-website
```
- `-d` runs the container in the background (detached mode).
- `-p 8080:80` maps port 8080 on your computer to port 80 in the container.

### 3. View Your Website
Open your browser and go to:
```
http://localhost:8080
```
You should see your static website served by NGINX.

### 4. Stop the Container
```bash
docker stop my-website
```

---
*Your website is now packaged in a portable container that runs anywhere Docker is installed.*
