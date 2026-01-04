import json
import duckdb
import requests
import re
from pathlib import Path

PROJECT_DIR = Path.cwd()
db_path = PROJECT_DIR / 'animal_shelter.duckdb'
conn = duckdb.connect(str(db_path), read_only=True)

# Load all 11 tests
with open(PROJECT_DIR / 'agent_ground_truth_test_cases.json', 'r') as f:
    test_cases = json.load(f)['test_cases']

with open(PROJECT_DIR / 'mindsdb_agent_config.json', 'r') as f:
    system_prompt = json.load(f)['system_prompt']

def mistral_text_to_sql(question, system_prompt):
    OLLAMA_URL = "http://127.0.0.1:11434"
    OLLAMA_MODEL = "mistral:latest"
    
    prompt = f"""{system_prompt}

Question: {question}

Generate SQL query:"""
    
    try:
        payload = {"model": OLLAMA_MODEL, "prompt": prompt, "stream": False, "temperature": 0.3}
        response = requests.post(f"{OLLAMA_URL}/api/generate", json=payload, timeout=90)
        
        if response.status_code == 200:
            generated_text = response.json()['response'].strip()
            sql_match = re.search(r'```(?:sql)?\s*(SELECT.*?);?\s*```', generated_text, re.DOTALL | re.IGNORECASE)
            if not sql_match:
                sql_match = re.search(r'(SELECT\s+.*?;)', generated_text, re.DOTALL | re.IGNORECASE)
            if sql_match:
                sql = sql_match.group(1).replace('```', '').strip()
                return sql + ';' if not sql.endswith(';') else sql
        return None
    except Exception as e:
        print(f"Exception: {e}")
        return None

print("\nFULL VALIDATION - ALL 11 TEST CASES")
print("="*80)

passed = 0
for test_case in test_cases:
    test_id = test_case['id']
    test_name = test_case['name']
    question = test_case['natural_language_question']
    expected_rows = len(test_case['expected_results'])
    
    print(f"\nQ{test_id}: {test_name}")
    print(f"  Question: {question[:60]}...")
    
    generated_sql = mistral_text_to_sql(question, system_prompt)
    
    if not generated_sql:
        print("  ERROR: Could not generate SQL")
        continue
    
    try:
        actual_count = len(conn.execute(generated_sql).df())
        if actual_count == expected_rows:
            print(f"  PASSED: {actual_count} rows")
            passed += 1
        else:
            print(f"  FAILED: Got {actual_count}, expected {expected_rows}")
    except Exception as e:
        print(f"  ERROR: {str(e)[:60]}")

print(f"\n{'='*80}")
print(f"Passed: {passed}/11 = {100*passed/11:.1f}%")
print(f"Previous baseline: 55% (6/11)")
improvement = (100*passed/11) - 55
if improvement > 0:
    print(f"IMPROVEMENT: +{improvement:.1f} percentage points!")
elif improvement < 0:
    print(f"DECLINE: {improvement:.1f} percentage points")
else:
    print(f"No change from baseline")
