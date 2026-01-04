import json

# Load the current config
with open('mindsdb_agent_config.json', 'r') as f:
    config = json.load(f)

# Get the current system prompt
prompt = config['system_prompt']

# Update the IMPORTANT RULES section to include proper animal type filtering
old_special_animals_rule = """5. For breed information, use dim_animal_attributes with primary_breed or breed_group column
   - CRITICAL: Some animals must be queried by primary_breed, NOT animal_type:
     * Rabbits: Use primary_breed LIKE 'Rabbit%' (stored as 'Rabbit Sh', 'Rabbit Lh', etc. in animal_type='Other')
     * Ducks: Use primary_breed LIKE 'Duck%' (found in BOTH 'Bird' and 'Dog' animal_types)
     * Goats: Use primary_breed LIKE 'Goat%' (stored in animal_type='Livestock')
   - For standard dog/cat breeds: Use exact match like a.primary_breed = 'Golden Retriever'"""

new_special_animals_rule = """5. For breed information, use dim_animal_attributes with primary_breed or breed_group column
   - CRITICAL: Some animals require BOTH animal_type AND primary_breed filters:
     * Rabbits: animal_type='Other' AND primary_breed LIKE 'Rabbit%' (e.g., 'Rabbit Sh', 'Rabbit Lh')
     * Ducks: animal_type='Bird' AND primary_breed LIKE 'Duck%' (MUST use animal_type to exclude 'Duck Tolling Retriever' dogs)
     * Goats: animal_type='Livestock' AND primary_breed LIKE 'Goat%'
   - For standard dog/cat breeds: Use exact match like a.primary_breed = 'Golden Retriever'"""

prompt = prompt.replace(old_special_animals_rule, new_special_animals_rule)

# Update the duck example to use animal_type='Bird'
old_duck_example = """Example 7 (DUCK QUERY):
Question: How many ducks came through the shelter?
Note: Ducks are in primary_breed as 'Duck', 'Duck Mix', 'Nova Scotia Duck Tolling Retriever', etc.
SQL:
SELECT COUNT(*) as total_ducks
            FROM fact_animal_outcome f
            JOIN dim_animal_attributes a ON f.animal_attributes_key = a.animal_attributes_key
            WHERE a.primary_breed LIKE 'Duck%'"""

new_duck_example = """Example 7 (DUCK QUERY):
Question: How many ducks came through the shelter?
Note: Use animal_type='Bird' to get actual ducks, not 'Duck Tolling Retriever' dogs
SQL:
SELECT COUNT(*) as total_ducks
            FROM fact_animal_outcome f
            JOIN dim_animal_attributes a ON f.animal_attributes_key = a.animal_attributes_key
            WHERE a.animal_type = 'Bird' AND a.primary_breed LIKE 'Duck%'"""

prompt = prompt.replace(old_duck_example, new_duck_example)

# Update the goat example to use animal_type='Livestock'
old_goat_example = """Example 8 (GOAT QUERY):
Question: How many goats were at the shelter?
Note: Goats are in animal_type='Livestock' with primary_breed LIKE 'Goat%'
SQL:
SELECT COUNT(*) as total_goats
            FROM fact_animal_outcome f
            JOIN dim_animal_attributes a ON f.animal_attributes_key = a.animal_attributes_key
            WHERE a.primary_breed LIKE 'Goat%'"""

new_goat_example = """Example 8 (GOAT QUERY):
Question: How many goats were at the shelter?
Note: Goats are in animal_type='Livestock' with primary_breed LIKE 'Goat%'
SQL:
SELECT COUNT(*) as total_goats
            FROM fact_animal_outcome f
            JOIN dim_animal_attributes a ON f.animal_attributes_key = a.animal_attributes_key
            WHERE a.animal_type = 'Livestock' AND a.primary_breed LIKE 'Goat%'"""

prompt = prompt.replace(old_goat_example, new_goat_example)

# Update the config
config['system_prompt'] = prompt
config['version'] = "1.4"
config['description'] = "SQL generation agent for Austin Animal Shelter analytics - Refined duck/goat/rabbit filtering to avoid false matches"

# Save the updated config
with open('mindsdb_agent_config.json', 'w') as f:
    json.dump(config, f, indent=2)

print("✓ Config updated successfully")
print(f"✓ Version updated to {config['version']}")
print(f"✓ Duck and Goat filtering refined to use animal_type for accuracy")
