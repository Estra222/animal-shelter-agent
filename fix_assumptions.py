import json

# Load the current config
with open('mindsdb_agent_config.json', 'r') as f:
    config = json.load(f)

# Get the current system prompt
prompt = config['system_prompt']

# Add a critical rule about not making assumptions
old_rule_10 = "10. Test queries locally before considering them final"

new_rules = """10. CRITICAL: Do NOT make assumptions about animal types. If the question asks about "cats", filter ONLY for 'Cat'. Do NOT add 'Dog' or other types.
    - If the question says "cats", use: a.animal_type = 'Cat'
    - If the question says "dogs", use: a.animal_type = 'Dog'  
    - Only include multiple animal types if explicitly mentioned (e.g., "cats and dogs")
11. Test queries locally before considering them final"""

prompt = prompt.replace(old_rule_10, new_rules)

# Update the config
config['system_prompt'] = prompt
config['version'] = "1.4"
config['description'] = "SQL generation agent for Austin Animal Shelter analytics - Added rule to avoid making assumptions about animal types"

# Save the updated config
with open('mindsdb_agent_config.json', 'w') as f:
    json.dump(config, f, indent=2)

print("✓ Config updated successfully")
print(f"✓ Version updated to {config['version']}")
print(f"✓ Added rule about not making assumptions about animal types")
