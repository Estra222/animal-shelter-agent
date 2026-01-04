import duckdb

# Open read-only to avoid lock
conn = duckdb.connect('animal_shelter.duckdb', read_only=True)

# Check what breed values actually exist
print('Sample primary_breed values with "Rabbit":')
result = conn.execute("SELECT DISTINCT primary_breed FROM dim_animal_attributes WHERE primary_breed LIKE '%Rabbit%' OR primary_breed LIKE '%rabbit%'").fetchall()
for row in result[:10]:
    print(f'  {row[0]}')

print('\nCount of rabbits by outcome type (case-insensitive):')
result = conn.execute("""
    SELECT o.outcome_type, COUNT(*) as count
    FROM fact_animal_outcome f
    JOIN dim_animal_attributes a ON f.animal_attributes_key = a.animal_attributes_key
    JOIN dim_outcome_type o ON f.outcome_key = o.outcome_key
    WHERE LOWER(a.primary_breed) LIKE '%rabbit%'
    GROUP BY o.outcome_type
""").fetchall()
for row in result:
    print(f'  {row[0]}: {row[1]}')

print('\nDirect query - rabbits adopted (case-insensitive):')
result = conn.execute("""
    SELECT COUNT(*) FROM fact_animal_outcome f
    JOIN dim_animal_attributes a ON f.animal_attributes_key = a.animal_attributes_key
    JOIN dim_outcome_type o ON f.outcome_key = o.outcome_key
    WHERE LOWER(a.primary_breed) LIKE '%rabbit%' AND o.outcome_type = 'Adoption'
""").fetchall()
print(f'  Total: {result[0][0]}')

# Test the exact query the agent generated
print('\nTesting agent-generated query (with "Rabbit" capital R):')
result = conn.execute("""
    SELECT COUNT(*) FROM fact_animal_outcome f
    JOIN dim_animal_attributes a ON f.animal_attributes_key = a.animal_attributes_key
    JOIN dim_outcome_type o ON f.outcome_key = o.outcome_key
    WHERE a.primary_breed = 'Rabbit' AND o.outcome_type = 'Adoption'
""").fetchall()
print(f'  Total: {result[0][0]}')
