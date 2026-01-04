import duckdb

conn = duckdb.connect('animal_shelter.duckdb', read_only=True)

# Check what animal_type ducks and goats are classified as
print('Ducks:')
result = conn.execute('''
    SELECT DISTINCT a.animal_type, COUNT(*) as count
    FROM fact_animal_outcome f
    JOIN dim_animal_attributes a ON f.animal_attributes_key = a.animal_attributes_key
    WHERE LOWER(a.primary_breed) LIKE '%duck%'
    GROUP BY a.animal_type
''').fetchall()
if result:
    for row in result:
        print(f'  {row[0]}: {row[1]}')
else:
    print('  (no ducks found)')

print('\nGoats:')
result = conn.execute('''
    SELECT DISTINCT a.animal_type, COUNT(*) as count
    FROM fact_animal_outcome f
    JOIN dim_animal_attributes a ON f.animal_attributes_key = a.animal_attributes_key
    WHERE LOWER(a.primary_breed) LIKE '%goat%'
    GROUP BY a.animal_type
''').fetchall()
if result:
    for row in result:
        print(f'  {row[0]}: {row[1]}')
else:
    print('  (no goats found)')

# Show sample breeds
print('\nSample duck breeds:')
result = conn.execute('''
    SELECT DISTINCT a.primary_breed
    FROM dim_animal_attributes a
    WHERE LOWER(a.primary_breed) LIKE '%duck%'
    LIMIT 5
''').fetchall()
if result:
    for row in result:
        print(f'  {row[0]}')
else:
    print('  (no duck breeds found)')

print('\nSample goat breeds:')
result = conn.execute('''
    SELECT DISTINCT a.primary_breed
    FROM dim_animal_attributes a
    WHERE LOWER(a.primary_breed) LIKE '%goat%'
    LIMIT 5
''').fetchall()
if result:
    for row in result:
        print(f'  {row[0]}')
else:
    print('  (no goat breeds found)')
