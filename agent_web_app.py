"""
Austin Animal Shelter Analytics Agent
Web interface for querying the animal shelter database with natural language
"""

import streamlit as st
import json
import duckdb
import requests
import re
from pathlib import Path

# Set page config
st.set_page_config(
    page_title="Animal Shelter Analytics Agent",
    page_icon="🐾",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom styling
st.markdown("""
    <style>
    .main {
        padding: 2rem;
    }
    .stTitle {
        color: #FF6B6B;
        font-size: 2.5em;
    }
    </style>
    """, unsafe_allow_html=True)

# ==============================================================================
# CONFIGURATION & SETUP
# ==============================================================================

PROJECT_DIR = Path(__file__).parent
DB_PATH = PROJECT_DIR / "animal_shelter.duckdb"
SCHEMA_PATH = PROJECT_DIR / "MINDSDB_SCHEMA_CONTEXT.txt"
AGENT_CONFIG_PATH = PROJECT_DIR / "mindsdb_agent_config.json"

OLLAMA_URL = "http://127.0.0.1:11434"
OLLAMA_MODEL = "mistral:latest"

# Load configuration
@st.cache_resource
def load_configuration():
    """Load all necessary configuration files"""
    config = {}
    
    # Load schema context
    try:
        with open(SCHEMA_PATH, 'r', encoding='utf-8') as f:
            config['schema_context'] = f.read()
    except Exception as e:
        st.error(f"Error loading schema: {e}")
        return None
    
    # Load agent config
    try:
        with open(AGENT_CONFIG_PATH, 'r', encoding='utf-8-sig') as f:
            config['agent_config'] = json.load(f)
    except Exception as e:
        st.error(f"Error loading agent config: {e}")
        return None
    
    return config

# Connect to database with retry logic
@st.cache_resource
def get_db_connection():
    """Create and cache database connection with retry logic"""
    import time
    
    max_retries = 3
    for attempt in range(max_retries):
        try:
            # Try to connect in read-only mode first
            conn = duckdb.connect(str(DB_PATH), read_only=True)
            # Test the connection
            conn.execute("SELECT 1").fetchone()
            st.success("✓ Database connected successfully")
            return conn
        except Exception as e:
            if attempt < max_retries - 1:
                st.warning(f"Attempt {attempt + 1} failed, retrying in 2 seconds...")
                time.sleep(2)
            else:
                st.error(f"Cannot connect to database after {max_retries} attempts: {str(e)}")
                st.info("**Solution**: Close the Jupyter notebook in VS Code and refresh this page")
                return None

# ==============================================================================
# SQL POST-PROCESSING TO FIX COMMON MISTRAL ERRORS
# ==============================================================================

def fix_common_sql_errors(sql):
    """Fix common column name mistakes made by Mistral"""
    import re
    
    # Fix gender-related column errors
    # s.gender -> s.sex_upon_outcome
    sql = re.sub(r'\bs\.gender\b', 's.sex_upon_outcome', sql, flags=re.IGNORECASE)
    # s.sex_name -> s.sex_upon_outcome
    sql = re.sub(r'\bs\.sex_name\b', 's.sex_upon_outcome', sql, flags=re.IGNORECASE)
    # s.sex_on_outcome -> s.sex_upon_outcome
    sql = re.sub(r'\bs\.sex_on_outcome\b', 's.sex_upon_outcome', sql, flags=re.IGNORECASE)
    
    # Fix ambiguous sex_key references (add table prefix if missing)
    # GROUP BY sex_key -> GROUP BY s.sex_key (when s alias is used)
    sql = re.sub(r'GROUP BY\s+sex_key\b', 'GROUP BY s.sex_key', sql, flags=re.IGNORECASE)
    
    # Fix date_key issues for date joins
    # f.date_key -> f.outcome_date_key
    sql = re.sub(r'\bf\.date_key\b', 'f.outcome_date_key', sql, flags=re.IGNORECASE)
    
    return sql

# ==============================================================================
# MISTRAL TEXT-TO-SQL FUNCTION
# ==============================================================================

def mistral_text_to_sql(question, schema_context, system_prompt):
    """Generate SQL from natural language using Mistral via Ollama"""
    
    prompt = f"""{system_prompt}

Question: {question}

Generate SQL query:"""
    
    try:
        payload = {
            "model": OLLAMA_MODEL,
            "prompt": prompt,
            "stream": False,
            "temperature": 0.3
        }
        
        response = requests.post(
            f"{OLLAMA_URL}/api/generate",
            json=payload,
            timeout=60
        )
        
        if response.status_code == 200:
            result = response.json()
            generated_text = result['response'].strip()
            
            # Extract SQL from response
            sql_match = re.search(r'```(?:sql)?\s*(SELECT.*?);?\s*```', generated_text, re.DOTALL | re.IGNORECASE)
            
            if not sql_match:
                sql_match = re.search(r'(SELECT\s+.*?;)', generated_text, re.DOTALL | re.IGNORECASE)
            
            if sql_match:
                sql = sql_match.group(1)
                sql = sql.replace('```', '').strip()
                if not sql.endswith(';'):
                    sql += ';'
                # Post-process SQL to fix common Mistral mistakes
                sql = fix_common_sql_errors(sql)
                return sql
            else:
                return None
        else:
            return None
            
    except requests.exceptions.ConnectionError:
        st.error("Cannot connect to Ollama. Make sure Ollama server is running on port 11434")
        return None
    except Exception as e:
        st.error(f"Error generating SQL: {str(e)}")
        return None

# ==============================================================================
# NATURAL LANGUAGE RESPONSE GENERATION
# ==============================================================================

def generate_natural_language_response(question, sql_query, result_df):
    """Generate a natural language summary of the query results"""
    
    # Convert dataframe to a readable format for the prompt
    results_summary = result_df.to_string(index=False)
    
    # Limit the results if too large
    if len(results_summary) > 2000:
        results_summary = results_summary[:2000] + "\n... (truncated)"
    
    prompt = f"""You are a helpful data analyst. A user asked this question:
"{question}"

This SQL query was executed:
{sql_query}

And produced these results:
{results_summary}

Provide a clear, concise, and human-friendly summary of what these results show. 
- Highlight key findings and patterns
- Use plain language that a non-technical person would understand
- Keep it to 2-3 sentences maximum
- Include specific numbers/percentages where relevant"""
    
    try:
        payload = {
            "model": OLLAMA_MODEL,
            "prompt": prompt,
            "stream": False,
            "temperature": 0.5  # Slightly higher temp for more natural language
        }
        
        response = requests.post(
            f"{OLLAMA_URL}/api/generate",
            json=payload,
            timeout=60
        )
        
        if response.status_code == 200:
            result = response.json()
            summary = result['response'].strip()
            return summary
        else:
            return None
            
    except requests.exceptions.ConnectionError:
        return None
    except Exception as e:
        return None

# ==============================================================================
# PAGE LAYOUT
# ==============================================================================

# Header
st.markdown("# 🐾 Austin Animal Shelter Analytics")
st.markdown("### Ask questions about the shelter in natural language")

# Load configuration
try:
    config = load_configuration()
    if config is None:
        st.stop()
    conn = get_db_connection()
    if conn is None:
        st.stop()
    system_prompt = config['agent_config']['system_prompt']
    schema_context = config['schema_context']
except Exception as e:
    st.error(f"Error loading configuration: {e}")
    st.info("**Solution**: \n1. Close the Jupyter notebook (`create_mindsdb_agent.ipynb`) in VS Code\n2. Refresh this browser page\n3. Try again")
    st.stop()

# ==============================================================================
# MAIN INTERFACE
# ==============================================================================

# Initialize session state for selected example
if 'selected_example' not in st.session_state:
    st.session_state.selected_example = ""

# Get initial value from selected example (if any)
initial_value = st.session_state.selected_example
st.session_state.selected_example = ""  # Clear it after reading

# Check Ollama connection
col1, col2 = st.columns([3, 1])
with col1:
    st.markdown("#### Ask a Question")
    question = st.text_input(
        "What would you like to know about the animal shelter?",
        value=initial_value,
        placeholder="e.g., What are the most common animal outcomes? How many dogs were adopted?",
        label_visibility="collapsed"
    )

with col2:
    st.markdown("#### System Status")
    try:
        response = requests.get(f"{OLLAMA_URL}/api/tags", timeout=2)
        if response.status_code == 200:
            st.success("✓ Ollama Ready")
        else:
            st.error("✗ Ollama Error")
    except:
        st.error("✗ Ollama Down")

st.markdown("---")

# Process question
if question:
    with st.spinner("🔄 Generating SQL query..."):
        # Generate SQL
        generated_sql = mistral_text_to_sql(question, schema_context, system_prompt)
        
        if generated_sql:
            st.success("✓ SQL generated successfully!")
            
            # Display the generated SQL
            with st.expander("📝 View Generated SQL", expanded=False):
                st.code(generated_sql, language="sql")
            
            # Execute the query
            try:
                with st.spinner("📊 Executing query..."):
                    if conn is None:
                        st.error("Database connection lost")
                    else:
                        result_df = conn.execute(generated_sql).df()
                
                if len(result_df) == 0:
                    st.warning("Query returned no results")
                else:
                    st.success(f"✓ Query returned {len(result_df)} rows")
                    
                    # Generate and display natural language summary FIRST
                    st.markdown("### 💬 Summary")
                    with st.spinner("✨ Generating summary..."):
                        summary = generate_natural_language_response(question, generated_sql, result_df)
                        if summary:
                            st.info(summary)
                        else:
                            st.info("(Unable to generate summary at this time)")
                    
                    st.markdown("---")
                    
                    # Display results table
                    st.markdown("### Results")
                    st.dataframe(result_df, use_container_width=True)
                    
                    # Download button
                    csv = result_df.to_csv(index=False)
                    st.download_button(
                        label="📥 Download Results as CSV",
                        data=csv,
                        file_name="query_results.csv",
                        mime="text/csv"
                    )
                    
            except Exception as e:
                st.error(f"Error executing SQL: {str(e)[:200]}")
        else:
            st.error("Failed to generate SQL. Please try a different question.")

st.markdown("---")

# ==============================================================================
# EXAMPLE QUERIES
# ==============================================================================

st.markdown("### 💡 Example Questions")

examples = [
    "What are the different animal outcomes and how many animals have each outcome?",
    "What are the top 5 primary breeds with the highest adoption rates?",
    "How do sick or injured animals typically fare?",
    "What are the most common intake types?",
    "What percentage of animals are spayed/neutered by age group?",
]

cols = st.columns(2)
for idx, example in enumerate(examples):
    col = cols[idx % 2]
    if col.button(f"📌 {example[:50]}...", use_container_width=True):
        st.session_state.selected_example = example
        st.rerun()

# ==============================================================================
# SIDEBAR
# ==============================================================================

with st.sidebar:
    st.markdown("## 📋 About")
    st.markdown("""
    This agent uses **Mistral LLM** (via Ollama) to convert natural language 
    questions into SQL queries, which are then executed against a DuckDB 
    database containing Austin Animal Shelter data.
    
    **Database:** Animal shelter intake and outcome data
    
    **Accuracy:** ~64% on validation test suite (7/11 tests passing)
    
    **Technology Stack:**
    - Mistral LLM (local via Ollama)
    - DuckDB (data storage)
    - Streamlit (web interface)
    """)
    
    st.markdown("---")
    st.markdown("## ⚙️ System Info")
    
    # Database stats
    st.subheader("Database")
    try:
        fact_count = conn.execute("SELECT COUNT(*) FROM fact_animal_outcome").fetchone()[0]
        st.metric("Fact Table Rows", f"{fact_count:,}")
    except:
        st.error("Cannot connect to database")
    
    # Ollama status
    st.subheader("Ollama")
    try:
        response = requests.get(f"{OLLAMA_URL}/api/tags", timeout=2)
        if response.status_code == 200:
            st.success("Connected")
    except:
        st.warning("Not running - web app may not work properly")

# ==============================================================================
# FOOTER
# ==============================================================================

st.markdown("---")
st.markdown("""
<div style="text-align: center; color: gray; font-size: 12px;">
    🐾 Austin Animal Shelter Analytics Agent | Powered by Mistral LLM
</div>
""", unsafe_allow_html=True)
