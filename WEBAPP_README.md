# Austin Animal Shelter Analytics Agent - Web Interface

A natural language SQL query interface for Austin Animal Shelter data powered by Mistral LLM.

## 🚀 Quick Start

### Prerequisites
- Python 3.10+
- Ollama installed with Mistral model
- MindsDB Server running

### Step 1: Ensure Ollama is Running
```bash
# In a terminal, start Ollama server (if not already running)
ollama serve
```

### Step 2: Ensure MindsDB is Running
```bash
# In another terminal, start MindsDB server (if not already running)
python -m mindsdb
```

### Step 3: Run the Web App
```bash
# In the project directory, activate the virtual environment
cd "c:\Users\mvzie\Documents\AI Agent Experiment"
.venv\Scripts\Activate.ps1

# Start Streamlit
streamlit run agent_web_app.py
```

The app will open in your browser at `http://localhost:8501`

## 📊 Features

- **Natural Language Queries**: Ask questions in plain English
- **Automatic SQL Generation**: Mistral LLM converts questions to SQL
- **Live Results**: View query results instantly
- **CSV Export**: Download results as CSV
- **Example Queries**: One-click example questions
- **SQL Preview**: View the generated SQL before execution

## 🎯 Example Questions

- "What are the different animal outcomes and how many animals have each outcome?"
- "What are the top 5 primary breeds with the highest adoption rates?"
- "How do sick or injured animals typically fare?"
- "What are the most common intake types?"
- "What percentage of animals are spayed/neutered by age group?"

## 📈 Current Performance

- **Validation Accuracy**: 64% on 11 comprehensive test cases
- **Passing Tests**: 7/11 test cases
- **Ollama Model**: Mistral (7B parameters, runs locally)
- **SQL Post-Processing**: Automatic correction of common LLM column name errors

## 🔧 Architecture

```
User Question
     ↓
[Streamlit Web Interface]
     ↓
[Mistral LLM (Ollama)]
     ↓
[SQL Query Generated]
     ↓
[DuckDB Execution]
     ↓
[Results Display]
```

## 💾 Data

- **Database**: animal_shelter.duckdb (DuckDB)
- **Fact Table**: fact_animal_outcome (172,044 rows)
- **Dimensions**: 5 dimension tables (dates, animals, outcomes, types, details)
- **Time Range**: 2013-2021

## ⚡ Performance Notes

- First query takes 30-60 seconds (Mistral model loading)
- Subsequent queries take 5-15 seconds
- No API costs (everything runs locally)
- Suitable for exploration and analytics

## 🐛 Troubleshooting

**"Cannot connect to Ollama"**
- Make sure `ollama serve` is running in a terminal
- Check that Mistral model is installed: `ollama list`
- Verify port 11434 is accessible

**"No results returned"**
- The generated SQL may not match your question perfectly
- Try rephrasing the question
- Check the generated SQL in the expanded view

**"Parser Error"**
- The LLM generated invalid SQL
- Try a simpler or differently worded question
- Complex questions may require manual SQL

## 📝 Files

- `agent_web_app.py` - Streamlit web application
- `create_mindsdb_agent.ipynb` - Agent training and validation notebook
- `animal_shelter.duckdb` - DuckDB database
- `MINDSDB_SCHEMA_CONTEXT.txt` - Database schema documentation
- `mindsdb_agent_config.json` - Agent configuration
- `agent_ground_truth_test_cases.json` - Validation test cases

## 🔐 Privacy & Security

- All processing happens locally on your machine
- No data is sent to external services
- Mistral LLM runs on your computer via Ollama
- Database is local DuckDB

## 📞 Support

For issues or questions, check:
1. Ollama status: `ollama status`
2. MindsDB status: Check that `python -m mindsdb` terminal shows no errors
3. Database: Verify `animal_shelter.duckdb` exists in the project directory
4. Web app logs: Check Streamlit terminal for error messages

## 🎓 Next Steps

To improve accuracy:
1. Refine the system prompt in the agent configuration
2. Add more example questions to the training set
3. Consider using a larger Mistral model: `ollama pull mistral:70b`
4. Switch to a more powerful LLM (OpenAI GPT-4, etc.)

---

**Built with**: Mistral LLM, Ollama, DuckDB, Streamlit, MindsDB
