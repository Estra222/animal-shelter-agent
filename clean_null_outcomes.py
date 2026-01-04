import duckdb

# Connect to DuckDB
conn = duckdb.connect('animal_shelter.duckdb')

print('Updating dim_outcome_type: replacing NULL outcome_type with Unknown')
conn.execute("UPDATE dim_outcome_type SET outcome_type = 'Unknown' WHERE outcome_type IS NULL")
print('  ✓ Updated rows')

print('\nVerifying update:')
result = conn.execute("SELECT outcome_key, outcome_type FROM dim_outcome_type WHERE outcome_type = 'Unknown'").fetchall()
print(f'  Records with Unknown outcome_type: {len(result)}')
for row in result:
    print(f'    outcome_key: {row[0]}')

print('\nAll distinct outcome_type values now:')
result2 = conn.execute('SELECT DISTINCT outcome_type FROM dim_outcome_type ORDER BY outcome_type').fetchall()
for row in result2:
    print(f'  {row[0]}')

conn.close()
print('\n✓ Database updated successfully')
