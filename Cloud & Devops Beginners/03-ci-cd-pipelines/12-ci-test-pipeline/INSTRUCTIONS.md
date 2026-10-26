# Instructions for Project 12: Build a CI Pipeline That Runs Tests on Every Commit

## Step-by-Step Guide

### 1. Create a GitHub Repository
- Go to [github.com](https://github.com) and sign in.
- Create a new repository named `area-calculator`.
- Initialize with a README.

### 2. Upload Your Files
Copy `calculator.py`, `test_calculator.py`, and the `.github/workflows/test.yml` file into your repository.

### 3. Commit and Push
```bash
git clone https://github.com/YOUR-USERNAME/area-calculator.git
cd area-calculator
# Copy the files here
git add .
git commit -m "Add calculator with unit tests"
git push origin main
```

### 4. Watch Tests Run
- Go to your repository → **Actions** tab.
- You'll see a workflow run automatically.
- Click into it to watch the tests execute step by step.
- ✅ Green checkmark = all tests passed!

### 5. Break a Test (Optional - for learning!)
- Open `calculator.py` and change `return length * width` to `return length + width` in `area_rectangle`.
- Push the change.
- Watch GitHub Actions catch the failing test!

---
*You now have an automated quality-control system that catches bugs before they happen.*
