"""
Generate ground truth test cases by executing queries against DuckDB
and storing results in JSON format for agent validation.
"""

import json
import duckdb
from pathlib import Path

# Connect to DuckDB
db_path = Path('animal_shelter.duckdb')
conn = duckdb.connect(str(db_path))

# Define test cases with their ground truth SQL
test_cases_config = [
    {
        "id": 1,
        "name": "Outcome Distribution",
        "business_scenario": "Understand the overall distribution of animal outcomes",
        "natural_language_question": "What are the different animal outcomes and how many animals have each outcome?",
        "sql": """
            SELECT outcome_type, COUNT(*) as total, 
                   ROUND(100.0 * COUNT(*) / SUM(COUNT(*)) OVER (), 1) as percentage,
                   ROUND(AVG(days_in_shelter), 1) as avg_days
            FROM fact_animal_outcome f
            JOIN dim_outcome_type o ON f.outcome_key = o.outcome_key
            GROUP BY outcome_type
            ORDER BY total DESC
        """
    },
    {
        "id": 2,
        "name": "Top Breed Groups Overall",
        "business_scenario": "Identify which breed groups are most common in shelter",
        "natural_language_question": "What are the top 10 most common breed groups in the shelter?",
        "sql": """
            SELECT breed_group, COUNT(*) as total,
                   ROUND(AVG(days_in_shelter), 1) as avg_days
            FROM fact_animal_outcome f
            JOIN dim_animal_attributes a ON f.animal_attributes_key = a.animal_attributes_key
            GROUP BY breed_group
            ORDER BY total DESC
            LIMIT 10
        """
    },
    {
        "id": 3,
        "name": "Adoption Success Rate by Primary Breed",
        "business_scenario": "Identify which breeds (across all animal types) are most likely to be adopted",
        "natural_language_question": "What are the top 5 primary breeds with the highest adoption rates?",
        "sql": """
            SELECT primary_breed,
                   COUNT(*) as total_animals,
                   SUM(CASE WHEN outcome_type = 'Adoption' THEN 1 ELSE 0 END) as adoptions,
                   ROUND(100.0 * SUM(CASE WHEN outcome_type = 'Adoption' THEN 1 ELSE 0 END) / COUNT(*), 1) as adoption_rate
            FROM fact_animal_outcome f
            JOIN dim_animal_attributes a ON f.animal_attributes_key = a.animal_attributes_key
            JOIN dim_outcome_type o ON f.outcome_key = o.outcome_key
            GROUP BY primary_breed
            ORDER BY adoption_rate DESC, total_animals DESC
            LIMIT 5
        """
    },
    {
        "id": 4,
        "name": "High Demand Animals (Short Stay Before Adoption/Transfer) by Breed",
        "business_scenario": "Identify adoptable pet breeds in highest demand with short availability windows",
        "natural_language_question": "What are the top 5 adoptable pet breeds with the shortest average stay before adoption or transfer?",
        "sql": """
            SELECT primary_breed,
                   COUNT(*) as count,
                   ROUND(AVG(days_in_shelter), 1) as avg_days_before_outcome
            FROM fact_animal_outcome f
            JOIN dim_animal_attributes a ON f.animal_attributes_key = a.animal_attributes_key
            JOIN dim_outcome_type o ON f.outcome_key = o.outcome_key
            WHERE outcome_type IN ('Adoption', 'Transfer')
              AND animal_type IN ('Dog', 'Cat', 'Rabbit', 'Livestock')
              AND primary_breed != 'Unknown'
            GROUP BY primary_breed
            ORDER BY avg_days_before_outcome ASC, count DESC
            LIMIT 5
        """
    },
    {
        "id": 5,
        "name": "High Need Animals (Longest Stay and Problem Conditions)",
        "business_scenario": "Identify animals with longest stays and health issues needing attention",
        "natural_language_question": "What are the top 10 combinations of primary breed and intake conditions with the longest average stay?",
        "sql": """
            SELECT primary_breed, intake_condition,
                   COUNT(*) as count,
                   ROUND(AVG(days_in_shelter), 1) as avg_days_in_shelter
            FROM fact_animal_outcome f
            JOIN dim_animal_attributes a ON f.animal_attributes_key = a.animal_attributes_key
            JOIN dim_intake_details id ON f.intake_details_key = id.intake_details_key
            GROUP BY primary_breed, intake_condition
            HAVING COUNT(*) >= 5
            ORDER BY avg_days_in_shelter DESC
            LIMIT 10
        """
    },
    {
        "id": 6,
        "name": "Sick and Injured Animals Outcomes",
        "business_scenario": "Understand outcomes for animals in poor health conditions (most common combinations)",
        "natural_language_question": "How do sick or injured animals typically fare? What are the most common outcome patterns for animals with health conditions?",
        "sql": """
            SELECT intake_condition, outcome_type, COUNT(*) as count,
                   ROUND(100.0 * COUNT(*) / SUM(COUNT(*)) OVER (PARTITION BY intake_condition), 1) as pct_of_condition
            FROM fact_animal_outcome f
            JOIN dim_intake_details id ON f.intake_details_key = id.intake_details_key
            JOIN dim_outcome_type o ON f.outcome_key = o.outcome_key
            WHERE has_condition_flag = 1
            GROUP BY intake_condition, outcome_type
            HAVING COUNT(*) >= 30
            ORDER BY count DESC
        """
    },
    {
        "id": 7,
        "name": "Stay Duration by Outcome",
        "business_scenario": "Understand how long animals typically stay for each outcome type",
        "natural_language_question": "For each outcome type, what is the distribution of how long animals stay?",
        "sql": """
            SELECT 
              CASE 
                WHEN days_in_shelter < 7 THEN '0-7 days'
                WHEN days_in_shelter < 30 THEN '8-29 days'
                WHEN days_in_shelter < 90 THEN '30-89 days'
                ELSE '90+ days'
              END as stay_duration,
              outcome_type,
              COUNT(*) as count
            FROM fact_animal_outcome f
            JOIN dim_outcome_type o ON f.outcome_key = o.outcome_key
            GROUP BY stay_duration, outcome_type
            ORDER BY CASE WHEN stay_duration = '0-7 days' THEN 1 
                         WHEN stay_duration = '8-29 days' THEN 2
                         WHEN stay_duration = '30-89 days' THEN 3
                         ELSE 4 END, count DESC
        """
    },
    {
        "id": 8,
        "name": "Monthly Outcome Trends 2016",
        "business_scenario": "Track outcome patterns across recent months",
        "natural_language_question": "What are the monthly outcome trends for 2016?",
        "sql": """
            SELECT d.month, outcome_type, COUNT(*) as count
            FROM fact_animal_outcome f
            JOIN dim_date d ON f.outcome_date_key = d.date_key
            JOIN dim_outcome_type o ON f.outcome_key = o.outcome_key
            WHERE d.year = 2016
            GROUP BY d.month, outcome_type
            ORDER BY d.month, outcome_type
        """
    },
    {
        "id": 9,
        "name": "Gender Distribution by Outcome",
        "business_scenario": "Understand if gender affects outcomes",
        "natural_language_question": "Do male and female animals have different outcome patterns?",
        "sql": """
            SELECT 
              CASE 
                WHEN is_male = 1 THEN 'Male'
                WHEN is_female = 1 THEN 'Female'
                ELSE 'Unknown'
              END as gender,
              outcome_type, 
              COUNT(*) as count,
              ROUND(100.0 * COUNT(*) / SUM(COUNT(*)) OVER (PARTITION BY CASE WHEN is_male = 1 THEN 'Male' WHEN is_female = 1 THEN 'Female' ELSE 'Unknown' END), 1) as pct_of_gender
            FROM fact_animal_outcome f
            JOIN dim_sex_on_outcome s ON f.sex_key = s.sex_key
            JOIN dim_outcome_type o ON f.outcome_key = o.outcome_key
            GROUP BY gender, outcome_type
            ORDER BY gender, count DESC
        """
    },
    {
        "id": 10,
        "name": "Intake Type Analysis",
        "business_scenario": "Understand which intake methods result in better outcomes",
        "natural_language_question": "What are the most common intake types and their outcome distributions?",
        "sql": """
            SELECT intake_type, COUNT(*) as total,
                   ROUND(100.0 * SUM(CASE WHEN outcome_type IN ('Adoption', 'Transfer', 'Return to Owner') THEN 1 ELSE 0 END) / COUNT(*), 1) as live_outcome_pct,
                   ROUND(AVG(days_in_shelter), 1) as avg_days
            FROM fact_animal_outcome f
            JOIN dim_intake_details id ON f.intake_details_key = id.intake_details_key
            JOIN dim_outcome_type o ON f.outcome_key = o.outcome_key
            GROUP BY intake_type
            ORDER BY total DESC
        """
    },
    {
        "id": 11,
        "name": "Reproductive Status by Age Group",
        "business_scenario": "Understand spay/neuter rates across different age groups",
        "natural_language_question": "By age group, what percentage of animals are spayed/neutered vs intact?",
        "sql": """
            SELECT 
              s.age_group,
              COUNT(*) as total_animals,
              SUM(CASE WHEN s.is_intact = 1 THEN 1 ELSE 0 END) as intact_count,
              ROUND(100.0 * SUM(CASE WHEN s.is_intact = 1 THEN 1 ELSE 0 END) / COUNT(*), 1) as intact_pct,
              SUM(CASE WHEN s.is_intact = 0 THEN 1 ELSE 0 END) as spayed_neutered_count,
              ROUND(100.0 * SUM(CASE WHEN s.is_intact = 0 THEN 1 ELSE 0 END) / COUNT(*), 1) as spayed_neutered_pct
            FROM fact_animal_outcome f
            JOIN dim_sex_on_outcome s ON f.sex_key = s.sex_key
            GROUP BY s.age_group
            ORDER BY 
              CASE 
                WHEN s.age_group = 'Under 1 Year' THEN 1
                WHEN s.age_group = '1-5 Years' THEN 2
                WHEN s.age_group = '5-10 Years' THEN 3
                WHEN s.age_group = 'Over 10 Years' THEN 4
                ELSE 5
              END
        """
    }
]

# Execute queries and build test cases with results
test_cases = []

print("Generating ground truth test cases...")
print("=" * 80)

for test_config in test_cases_config:
    print(f"\nTest {test_config['id']}: {test_config['name']}")
    
    try:
        # Execute the query
        results = conn.execute(test_config['sql']).fetchall()
        columns = [desc[0] for desc in conn.description]
        
        # Convert to list of dicts
        result_dicts = [dict(zip(columns, row)) for row in results]
        
        # Convert any float values to proper format for JSON
        for result in result_dicts:
            for key, value in result.items():
                if isinstance(value, float):
                    result[key] = round(value, 2)
        
        # Build test case
        test_case = {
            "id": test_config['id'],
            "name": test_config['name'],
            "business_scenario": test_config['business_scenario'],
            "natural_language_question": test_config['natural_language_question'],
            "ground_truth_sql": test_config['sql'].strip(),
            "expected_columns": columns,
            "expected_results": result_dicts,
            "result_count": len(result_dicts)
        }
        
        test_cases.append(test_case)
        print(f"  ✓ Executed successfully - {len(result_dicts)} rows")
        print(f"  Columns: {', '.join(columns)}")
        
    except Exception as e:
        print(f"  ✗ Error: {e}")

# Save to JSON file
output = {
    "project": "Austin Animal Shelter",
    "description": "Ground truth test cases for MindsDB agent validation",
    "total_test_cases": len(test_cases),
    "test_cases": test_cases
}

with open('agent_ground_truth_test_cases.json', 'w', encoding='utf-8') as f:
    json.dump(output, f, indent=2, ensure_ascii=False)

print("\n" + "=" * 80)
print(f"✓ Generated {len(test_cases)} test cases")
print("✓ Saved to: agent_ground_truth_test_cases.json")
print("=" * 80)

# Close connection
conn.close()
