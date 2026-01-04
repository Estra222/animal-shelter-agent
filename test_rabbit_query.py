import json
import duckdb
from mindsdb.integrations.handlers.ollama_handler.ollama_handler import OllamaHandler

# Load the updated agent config
with open('mindsdb_agent_config.json', 'r') as f:
    config = json.load(f)

# For testing, we'll manually use Ollama to generate SQL based on the system prompt
import requests
import json as json_lib

def test_rabbit_query():
    # The question
    question = "How many rabbits were adopted from the shelter?"
    
    # Call Ollama with the system prompt from our config
    system_prompt = config['system_prompt']
    
    payload = {
        "model": "mistral",
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"Generate a DuckDB SQL query to answer: {question}"}
        ],
        "temperature": config['temperature'],
        "stream": False
    }
    
    try:
        response = requests.post(
            "http://localhost:11434/api/chat",
            json=payload,
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            sql = result['message']['content']
            
            # Extract just the SQL part if there's explanation text
            if 'SELECT' in sql:
                sql = sql[sql.index('SELECT'):].strip()
                if '```' in sql:
                    sql = sql.split('```')[0].strip()
            
            print(f"Question: {question}\n")
            print(f"Generated SQL:\n{sql}\n")
            
            # Execute the query
            conn = duckdb.connect('animal_shelter.duckdb', read_only=True)
            try:
                result = conn.execute(sql).fetchall()
                print(f"✓ Query executed successfully")
                print(f"Result: {result}")
                
                # Compare to expected (should be 294 + 1 = 295 if including Rto-Adopt)
                expected = 294
                actual = result[0][0] if result and result[0] else 0
                print(f"\nExpected: {expected} adoptions")
                print(f"Actual: {actual} adoptions")
                if actual == expected:
                    print("✓ CORRECT!")
                else:
                    print(f"✗ Incorrect (off by {abs(actual - expected)})")
            except Exception as e:
                print(f"✗ Query execution failed: {e}")
        else:
            print(f"Ollama error: {response.status_code}")
    except requests.ConnectionError:
        print("✗ Cannot connect to Ollama on localhost:11434")
        print("  Is Ollama running? Try: ollama serve")
    except Exception as e:
        print(f"✗ Error: {e}")

if __name__ == "__main__":
    test_rabbit_query()
