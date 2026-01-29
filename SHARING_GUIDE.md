# How to Share the Animal Shelter Analytics Agent

## 🎯 Quick Share Options

### Option 1: Share the Web App URL (Easiest)
If others are on your local network:
1. Keep the Streamlit app running (`streamlit run agent_web_app.py`)
2. Share the **Network URL**: `http://192.168.1.4:8501` (or your IP address)
3. Others can access it from their browser

### Option 2: Share the Entire Project (Self-Contained)
Send the entire `AI Agent Experiment` folder to others:
1. Zip the project folder
2. They need to install: Python, Ollama, MindsDB
3. They run the startup scripts locally

### Option 3: Cloud Deployment (Coming Soon)
Deploy to cloud services:
- Heroku
- AWS
- Azure
- Streamlit Cloud

---

## 📋 Requirements for Others to Run

### System Requirements
- Windows/Mac/Linux with Python 3.10+
- Minimum 8GB RAM
- At least 10GB disk space (for Ollama models)
- Internet connection (for initial setup)

### Software Dependencies

Users need to install:

1. **Ollama** (Free)
   - Download: https://ollama.ai
   - Pull Mistral: `ollama pull mistral`

2. **Python** (Free)
   - Download: https://python.org
   - Version 3.10 or higher

3. **Project Dependencies** (Free)
   ```bash
   pip install -r requirements.txt
   ```

---

## 🚀 Step-by-Step Setup Instructions (For Recipients)

### Step 1: Download Project
```bash
# Get the project folder from wherever you shared it
cd AI\ Agent\ Experiment
```

### Step 2: Install Ollama
1. Go to https://ollama.ai
2. Download and install for your OS
3. Open terminal and run: `ollama pull mistral`
4. Start Ollama: `ollama serve`

### Step 3: Install Python Dependencies
```bash
# Create virtual environment
python -m venv .venv

# Activate it
# On Windows:
.venv\Scripts\Activate.ps1

# On Mac/Linux:
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Step 4: Start Services

**Terminal 1** (Ollama - already running from step 2)
```bash
ollama serve
```

**Terminal 2** (MindsDB)
```bash
python -m mindsdb
```

**Terminal 3** (Web App)
```bash
# Activate venv first
.venv\Scripts\Activate.ps1

# Run the app
streamlit run agent_web_app.py
```

### Step 5: Access the App
- Open browser to: **http://localhost:8501**
- Start asking questions!

---

## 📦 Creating Requirements File

If you haven't already, create `requirements.txt`:

```txt
streamlit>=1.28.0
duckdb>=0.9.0
requests>=2.31.0
pandas>=2.0.0
mindsdb-sdk>=1.0.0
```

Save this file in the project directory.

---

## 🌐 Sharing Methods

### Method 1: Email/File Share (Small Team)
1. Zip the project folder
2. Share via email or file sharing service
3. Recipients unzip and follow setup above

### Method 2: GitHub (Professional)
1. Create GitHub repository
2. Upload entire project
3. Share GitHub link
4. Recipients clone and set up

### Method 3: Cloud Deployment
**Streamlit Cloud** (Free, easiest):
1. Push code to GitHub
2. Connect to Streamlit Cloud
3. Share public link
4. Anyone can use (no local setup)

**Note**: Streamlit Cloud version would need Ollama/MindsDB hosted separately

---

## 💡 Quick Share Checklist

- [ ] All required files included:
  - [ ] `agent_web_app.py`
  - [ ] `animal_shelter.duckdb`
  - [ ] `MINDSDB_SCHEMA_CONTEXT.txt`
  - [ ] `mindsdb_agent_config.json`
  - [ ] `agent_ground_truth_test_cases.json`
  - [ ] `requirements.txt`
  - [ ] `WEBAPP_README.md`

- [ ] Documentation included:
  - [ ] Setup instructions
  - [ ] Troubleshooting guide
  - [ ] Example questions

- [ ] Recipients know:
  - [ ] System requirements
  - [ ] Startup sequence (Ollama → MindsDB → App)
  - [ ] Where to find help

---

## 🆘 Support & Troubleshooting

### Common Issues for Recipients

**"Module not found" error**
```bash
# Solution: Reinstall packages
pip install -r requirements.txt --upgrade
```

**"Cannot connect to Ollama"**
```bash
# Solution: Make sure Ollama is running
ollama serve
```

**"DuckDB connection failed"**
```bash
# Solution: Verify database file exists
ls animal_shelter.duckdb  # On Mac/Linux
dir animal_shelter.duckdb  # On Windows
```

**"Streamlit not found"**
```bash
# Solution: Activate virtual environment
# Windows:
.venv\Scripts\Activate.ps1

# Mac/Linux:
source .venv/bin/activate
```

---

## 📊 System Information to Share

Share this with users so they know what they're getting:

```
SYSTEM SPECIFICATIONS
═══════════════════════════════════════

LLM Model:         Mistral 7B (local)
Database:          DuckDB (172K rows)
Interface:         Streamlit Web App
Test Accuracy:     64% (7/11 test cases)
API Costs:         $0/month
Setup Time:        ~15 minutes
First Query Time:  30-60 seconds
Subsequent Queries: 5-15 seconds

REQUIRED DISK SPACE
═══════════════════════════════════════
Ollama + Mistral:  ~5GB
Project Files:     ~200MB
Total:             ~5.2GB

NO EXTERNAL DEPENDENCIES
═══════════════════════════════════════
✓ All processing is local
✓ No API keys required
✓ No internet needed after setup
✓ No data leaves your computer
✓ No subscription fees
```

---

## 🎓 Teaching Others

If sharing with non-technical users:

1. **Simple Explanation**
   - "It's like Google search for database queries"
   - "Type a question, get results instantly"
   - "No coding knowledge needed"

2. **Demo First**
   - Show the web interface working
   - Ask one simple question
   - Show the results

3. **Let Them Try**
   - Have them ask a question themselves
   - Help troubleshoot first issues
   - Build confidence

---

## 🚀 Next: Deployment Options

Once others are using it locally, consider:

### Heroku Deployment
- Free tier available
- 30-second startup time
- Easy to share public link

### AWS Deployment
- More control
- Better for high traffic
- Costs money

### Streamlit Cloud
- Easiest option
- Free for open source
- Public dashboard

---

## ❓ FAQ for Users

**Q: Is my data safe?**
A: Yes! Everything runs on your computer. No data leaves your machine.

**Q: Do I need internet?**
A: Only for initial setup. After that, everything works offline.

**Q: Will it always give correct answers?**
A: No. It's 64% accurate. Some questions may need rephrasing or manual SQL.

**Q: Can multiple people use it at once?**
A: Yes, if they're on the same network and know the IP address.

**Q: What if I have a slow computer?**
A: It needs at least 8GB RAM. Queries will be slower on weaker machines.

---

## 📝 Share This Template

Create a `SETUP_GUIDE.md` for recipients:

```markdown
# Austin Animal Shelter Analytics Agent - Setup Guide

Hi! You've received a Natural Language SQL query interface for 
animal shelter data. Here's how to set it up:

## Quick Start (15 minutes)

### 1. Install Ollama
- Go to https://ollama.ai
- Download and install
- Run: `ollama pull mistral`
- Start: `ollama serve`

### 2. Install Python Packages
```bash
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### 3. Start Services
- Terminal 1: `ollama serve` (from step 1)
- Terminal 2: `python -m mindsdb`
- Terminal 3: `.venv\Scripts\Activate.ps1` then `streamlit run agent_web_app.py`

### 4. Use It
- Open: http://localhost:8501
- Ask a question
- Get results!

## Questions?
See `WEBAPP_README.md` for detailed documentation.
```

---

**Ready to share? You're all set!** 🎉
