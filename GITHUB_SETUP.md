# GitHub Setup Guide

## 🚀 Uploading to GitHub: https://github.com/TheBlackLabel55/Lazi-sniper

This guide will help you upload your Lazada Sniper Bot to your GitHub repository.

---

## ⚡ Quick Method (Automated)

### **For Windows:**

1. Open Command Prompt in the project folder
2. Run:
   ```batch
   push_to_github.bat
   ```
3. Follow the prompts
4. Sign in to GitHub when asked

### **For Mac/Linux:**

1. Open Terminal in the project folder
2. Make script executable:
   ```bash
   chmod +x push_to_github.sh
   ```
3. Run:
   ```bash
   ./push_to_github.sh
   ```
4. Follow the prompts
5. Sign in to GitHub when asked

---

## 📝 Manual Method (Step-by-Step)

If the automated script doesn't work, follow these manual steps:

### **Step 1: Install Git (if not already)**

**Windows:**
- Download from: https://git-scm.com/download/win
- During install: Check "Add Git to PATH"

**Mac:**
```bash
brew install git
```

**Linux:**
```bash
sudo apt-get install git
```

### **Step 2: Configure Git (First Time Only)**

```bash
# Set your name
git config --global user.name "Your Name"

# Set your email (use your GitHub email)
git config --global user.email "your-email@example.com"
```

### **Step 3: Initialize Repository**

Open terminal in your project folder (`C:\Users\65964\Desktop\Lazada`):

```bash
# Initialize git
git init

# Add all files
git add .

# Create initial commit
git commit -m "Initial commit: Lazada Sniper Bot with Store Monitor"
```

### **Step 4: Connect to GitHub**

```bash
# Set branch name to main
git branch -M main

# Add your GitHub repository as remote
git remote add origin https://github.com/TheBlackLabel55/Lazi-sniper.git
```

### **Step 5: Push to GitHub**

```bash
# Push to GitHub
git push -u origin main
```

**Note:** You'll be asked to sign in to GitHub. Use one of these methods:
- GitHub username and password (if 2FA not enabled)
- Personal Access Token (recommended)
- GitHub CLI authentication

---

## 🔑 GitHub Authentication

### **Method 1: Personal Access Token (Recommended)**

1. Go to: https://github.com/settings/tokens
2. Click "Generate new token" → "Generate new token (classic)"
3. Give it a name: "Lazada Sniper Bot"
4. Check scopes:
   - ✅ `repo` (Full control of private repositories)
5. Click "Generate token"
6. **Copy the token** (you won't see it again!)
7. When pushing, use:
   - Username: `TheBlackLabel55`
   - Password: `paste-your-token-here`

### **Method 2: GitHub CLI**

```bash
# Install GitHub CLI
# Windows: winget install GitHub.cli
# Mac: brew install gh
# Linux: See https://cli.github.com/

# Authenticate
gh auth login

# Then push normally
git push -u origin main
```

---

## ✅ Verify Upload

After pushing, check:

1. Go to: https://github.com/TheBlackLabel55/Lazi-sniper
2. You should see:
   - ✅ All your files
   - ✅ README.md displayed
   - ✅ Folders: `bot/`, `learning/`, `examples/`, etc.

---

## 🔄 Updating Repository (Future Changes)

After making changes to your code:

```bash
# Add changed files
git add .

# Commit with description
git commit -m "Updated store monitor keywords"

# Push to GitHub
git push
```

---

## 📦 Cloning to Another Device

On your other device:

```bash
# Clone the repository
git clone https://github.com/TheBlackLabel55/Lazi-sniper.git

# Enter folder
cd Lazi-sniper

# Install dependencies
pip install -r requirements.txt
playwright install chromium

# Run!
python main_store_sniper.py
```

---

## 🐛 Troubleshooting

### **Error: "git: command not found"**

**Solution:** Install Git
- Windows: https://git-scm.com/download/win
- Mac: `brew install git`
- Linux: `sudo apt-get install git`

### **Error: "remote origin already exists"**

**Solution:**
```bash
git remote remove origin
git remote add origin https://github.com/TheBlackLabel55/Lazi-sniper.git
git push -u origin main
```

### **Error: "Authentication failed"**

**Solution:** Use Personal Access Token instead of password
1. Generate token: https://github.com/settings/tokens
2. Use token as password when pushing

### **Error: "Permission denied"**

**Solution:** Make sure you're logged into the correct GitHub account
```bash
# Check current user
git config user.name

# Change if needed
git config --global user.name "TheBlackLabel55"
```

### **Error: "failed to push some refs"**

**Solution:** Pull first, then push
```bash
git pull origin main --allow-unrelated-histories
git push -u origin main
```

---

## 🔒 Security Notes

### **What's Already Protected:**

Your `.gitignore` file already prevents uploading:
- ✅ Passwords and credentials
- ✅ `__pycache__/` folders
- ✅ Screenshots with personal info
- ✅ Environment variables (`.env` files)
- ✅ IDE settings

### **What WILL Be Uploaded:**

- ✅ All `.py` source code files
- ✅ Documentation (`.md` files)
- ✅ Configuration templates
- ✅ Requirements and dependencies
- ✅ Tutorial scripts

### **Safe to Share:**

This is educational code and safe to make public. However:
- ⚠️ Don't add real Lazada credentials to any file
- ⚠️ Don't commit screenshots with personal info
- ⚠️ Don't include your actual product URLs or store names in committed code

---

## 📊 Repository Structure

After uploading, your GitHub repo will show:

```
Lazi-sniper/
├── 📄 README.md
├── 📄 STORE_SNIPER_GUIDE.md
├── 📄 GETTING_STARTED.md
├── 📄 requirements.txt
├── 📄 main.py
├── 📄 main_store_sniper.py
├── 📁 bot/
│   ├── monitor.py
│   ├── store_monitor.py
│   ├── cart.py
│   └── checkout.py
├── 📁 learning/
│   ├── 01_html_css_basics.py
│   ├── 02_web_automation.py
│   ├── 03_python_essentials.py
│   └── 04_network_analysis.py
├── 📁 examples/
│   ├── inspect_lazada.py
│   ├── test_timing.py
│   └── test_store_monitor.py
└── 📁 config/
    └── settings.py
```

---

## 🎉 Success!

Once uploaded, you can:

1. ✅ **View your code online**: https://github.com/TheBlackLabel55/Lazi-sniper
2. ✅ **Clone to other devices**: `git clone https://github.com/TheBlackLabel55/Lazi-sniper.git`
3. ✅ **Track changes**: Git history shows all modifications
4. ✅ **Collaborate**: Share with others or get help
5. ✅ **Backup**: Your code is safely stored on GitHub

---

## 🔗 Quick Links

- **Your Repository**: https://github.com/TheBlackLabel55/Lazi-sniper
- **GitHub Docs**: https://docs.github.com/en/get-started
- **Git Cheat Sheet**: https://education.github.com/git-cheat-sheet-education.pdf

---

## 💡 Next Steps

After uploading:

1. Add a star ⭐ to your own repository (for fun!)
2. Edit README.md on GitHub to add custom description
3. Clone to another device to test
4. Make changes and practice pushing updates

Good luck! 🚀

