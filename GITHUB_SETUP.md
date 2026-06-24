# GitHub Setup Guide for BA Engine Orchestrator

## Step 1: Create GitHub Repository

### Manual Steps (Visual):

1. Go to: https://github.com/new
2. Fill in:
   - **Repository name:** `ba-orchestrator`
   - **Description:** "Convert unstructured client requests to structured SRS documents using AI and FastAPI"
   - **Visibility:** Public (for your portfolio)
   - **DO NOT initialize with README, .gitignore, or license** (you already have these)
3. Click "Create repository"

### After Creation:

You'll see a page with setup instructions. Copy-paste them OR follow the commands below.

---

## Step 2: Connect Local Repo to GitHub

After creating the repo on GitHub, run these commands:

```bash
cd d:\BA-Orchestrator

# Add GitHub as the remote origin
git remote add origin https://github.com/YOUR-USERNAME/ba-orchestrator.git

# Rename main branch from 'master' to 'main' (GitHub standard)
git branch -M main

# Push code to GitHub
git push -u origin main
```

**Replace `YOUR-USERNAME` with your actual GitHub username!**

---

## Step 3: Verify on GitHub

After pushing:
1. Go to https://github.com/YOUR-USERNAME/ba-orchestrator
2. You should see all your files
3. Green "Code" button should be available

---

## Step 4: GitHub Desktop Setup

### Install GitHub Desktop (if not already installed):
- Download: https://desktop.github.com/

### Clone via GitHub Desktop:
1. Open GitHub Desktop
2. Click "File" → "Clone repository"
3. Select your `ba-orchestrator` repo
4. Choose local path: `d:\BA-Orchestrator` (or similar)
5. Click "Clone"

### Now you can:
- See changes visually in GitHub Desktop
- Create branches easily
- Make commits with nice UI
- Create Pull Requests

---

## Step 5: Create Feature Branch

Professional workflow:
1. Never commit directly to `main`
2. Create a `feature/` branch for each task
3. Make commits there
4. Create Pull Request (PR) to review before merging

### To create a feature branch in GitHub Desktop:

1. Click "Current Branch" at the top
2. Click "New Branch"
3. Name it: `feature/api-testing` or `feature/documentation`
4. Make sure it's based on `main`
5. Click "Create Branch"

---

## Git Workflow (Professional Practice)

```
main branch (production-ready code)
    ↑
    └─── feature/api-testing
    │         ├─ commit 1
    │         ├─ commit 2
    │         └─ Pull Request → merged to main
    │
    └─── feature/documentation
              ├─ commit 1
              ├─ commit 2
              └─ Pull Request → merged to main
```

---

## Commit Message Best Practices

Good commit messages:

❌ Bad:
```
fix stuff
updated code
more changes
```

✅ Good:
```
Fix: Correct Gemini model name from gemini-pro to gemini-2.5-flash

This resolves the 404 error where the old model was no longer available.
Tested with sample input and verified SRS generation works correctly.
```

Structure:
```
[Type]: [Short description - max 50 chars]

[Optional detailed explanation]
[What was changed and why]
[Testing done]
```

Types: `feat:`, `fix:`, `docs:`, `test:`, `refactor:`, `chore:`

---

## Commands for Command Line (Alternative)

If you prefer CLI over GitHub Desktop:

```bash
# Check current branch
git branch

# Create and switch to new branch
git checkout -b feature/your-feature-name

# Make changes, then...
git add .
git commit -m "Meaningful message here"

# Push branch to GitHub
git push -u origin feature/your-feature-name

# Create PR (GitHub will show a prompt on the website)
```

---

## Next Steps After Pushing

1. ✅ Push to GitHub
2. ✅ Create feature branch
3. ✅ Make organized commits
4. ✅ Create Pull Request
5. ✅ Review changes
6. ✅ Merge to main
7. ✅ Share GitHub URL with reviewers/portfolio

---

## Troubleshooting

### "fatal: remote origin already exists"
```bash
git remote remove origin
git remote add origin https://github.com/YOUR-USERNAME/ba-orchestrator.git
```

### "fatal: You are not currently on a branch"
```bash
git checkout -b main
git push -u origin main
```

### "Permission denied (publickey)"
- Make sure SSH key is configured
- Or use HTTPS instead of SSH
- Check: https://github.com/settings/keys

