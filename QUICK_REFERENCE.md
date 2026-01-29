# 🐾 QUICK REFERENCE CARD

## ⚡ 30-Second Startup

```bash
# Terminal 1: Start Ollama (if not already running)
ollama serve

# Terminal 2: Start MindsDB
python -m mindsdb

# Terminal 3: Run Web App
cd "c:\Users\mvzie\Documents\AI Agent Experiment"
.venv\Scripts\Activate.ps1
streamlit run agent_web_app.py
```

**Then open browser**: http://localhost:8501

---

## 🎯 What It Does

```
Ask Questions in English → AI Generates SQL → See Results
```

Example:
```
"What are the most common animal outcomes?"
     ↓
SELECT outcome_type, COUNT(*) as count...
     ↓
Outcome Distribution: Adoption (6), Transfer (3), ... (12 rows)
```

---

## ✅ System Status Checks

### Is Ollama Running?
```bash
curl http://127.0.0.1:11434/api/tags
```
✅ Should return list of models (mistral:latest)

### Is MindsDB Running?
```
http://127.0.0.1:47334
```
✅ Should open MindsDB dashboard in browser

### Is Web App Working?
```
http://localhost:8501
```
✅ Should show web interface

---

## 📊 Test Results Summary

```
Total Tests:     11
Passing:         7  (64% accuracy)
Failing:         4

Best Performance:   Simple aggregates, gender queries
Needs Work:         Complex joins, date-based queries
```

---

## 🎨 Web App Features

| Feature | How to Use |
|---------|-----------|
| Ask Question | Type in input box |
| View SQL | Click "View Generated SQL" |
| See Results | Scroll down |
| Download CSV | Click "Download Results" |
| Example Queries | Click any example button |

---

## 🚨 Common Issues & Fixes

| Problem | Solution |
|---------|----------|
| "Cannot connect to Ollama" | Run `ollama serve` |
| "Database not found" | Check `animal_shelter.duckdb` exists |
| "Streamlit not found" | Activate venv: `.venv\Scripts\Activate.ps1` |
| "Invalid SQL" | Rephrase the question |
| "No results" | Try simpler question |

---

## 📁 Key Files

| File | Purpose |
|------|---------|
| `agent_web_app.py` | Main web interface |
| `animal_shelter.duckdb` | Database (172K rows) |
| `mindsdb_agent_config.json` | Agent settings |
| `MINDSDB_SCHEMA_CONTEXT.txt` | Database schema |

---

## 💻 System Requirements

- Windows/Mac/Linux
- Python 3.10+
- Ollama installed
- 8GB+ RAM
- 10GB disk space

---

## 🌐 Share With Others

### Local Network Share
Users on your WiFi can access:
```
http://[YOUR_IP]:8501
```

### Full Project Share
Send the entire folder + sharing guide:
```
See: SHARING_GUIDE.md
```

---

## 📚 Documentation

| Document | Purpose |
|----------|---------|
| `FINAL_STATUS.md` | Complete overview |
| `PROJECT_COMPLETION_SUMMARY.md` | Project summary |
| `WEBAPP_README.md` | Web app details |
| `SHARING_GUIDE.md` | How to share |

---

## ⏱️ Performance

| Operation | Time |
|-----------|------|
| First query | 30-60s |
| Subsequent | 5-15s |
| Result export | <1s |

---

## 🎓 Example Questions

```
✅ "What are the animal outcomes?"
✅ "Top 5 breeds by adoption?"
✅ "Sick animals outcomes?"
✅ "Age group breakdown?"
✅ "Monthly trends?"
```

---

## 🔥 Pro Tips

1. **First query is slow** - Model is loading (30-60s)
2. **Keep Ollama running** - Leave it in background
3. **Simple questions work best** - Specific & clear
4. **Check the SQL** - Learn by viewing generated queries
5. **Export results** - Download CSV for further analysis

---

## 📞 Emergency Help

Can't get it working?

1. Check all 3 services are running:
   - Ollama: `ollama serve`
   - MindsDB: `python -m mindsdb`
   - Streamlit: `streamlit run agent_web_app.py`

2. Check files exist:
   - `animal_shelter.duckdb`
   - `mindsdb_agent_config.json`
   - `agent_web_app.py`

3. Try in clean terminal:
   ```bash
   cd "c:\Users\mvzie\Documents\AI Agent Experiment"
   .venv\Scripts\Activate.ps1
   streamlit run agent_web_app.py --logger.level=debug
   ```

---

## ✨ Success = 3 Things Working

```
✅ Ollama running (http://127.0.0.1:11434)
✅ MindsDB running (http://127.0.0.1:47334)
✅ Streamlit running (http://localhost:8501)
```

If all 3 are working, the system is operational!

---

**Last Updated**: January 2, 2026  
**Status**: 🟢 Operational  
**Version**: 1.0  

**Keep this card handy for quick reference!**
