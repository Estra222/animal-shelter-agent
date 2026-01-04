import json
from pathlib import Path

# Test that config loads without errors
AGENT_CONFIG_PATH = Path('mindsdb_agent_config.json')

try:
    with open(AGENT_CONFIG_PATH, 'r', encoding='utf-8-sig') as f:
        config = json.load(f)
    print('✓ Config loads successfully')
    print(f'✓ Config version: {config.get("version", "unknown")}')
    print(f'✓ Config has system_prompt: {len(config.get("system_prompt", "")) > 0}')
    print(f'✓ Temperature: {config.get("temperature", "unknown")}')
    print(f'✓ Description: {config.get("description", "")[:60]}...')
except Exception as e:
    print(f'✗ Error: {e}')
