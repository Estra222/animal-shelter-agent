# Austin Animal Shelter Outcomes — Data Agent & Dimensional Model

**Project Status:** ✅ Star Schema Complete & Validated | Ground Truth Tests Generated | Ready for Agent Validation  
**Last Updated:** January 1, 2026  
**Current Phase:** Step 8 - MindsDB Integration & Agent Validation

## Purpose

Build a **data agent that helps potential adopters understand shelter outcome trends** — empowering them to save animals at risk of extended stays or euthanasia, and to ask better questions when visiting the shelter.

This project demonstrates **professional Kimball-style dimensional modeling** using a modern, local-first toolchain with complete test-driven development.

## Who Is This For?

- Potential adopters who want to make an informed, compassionate choice
- People interested in rescuing animals that are statistically at higher risk
- Anyone curious about shelter dynamics before visiting in person
- Data engineers learning dimensional modeling best practices

## What the Agent Does

- Answers questions about **historical outcome patterns** (not live inventory)
- Identifies which animal types, breeds, ages, or conditions tend to have longer stays or worse outcomes
- Highlights **high-demand pets** that get adopted quickly — so users know to check the shelter frequently for new arrivals
- Helps users understand what to ask shelter staff (e.g., "Do you have any senior cats that have been here a while?")

---

## Project Completion Summary

### ✅ Completed Phases

**Phase 1: Data Acquisition & Feature Engineering (COMPLETE)**
- Downloaded Austin Animal Center Outcomes (173,775 records)
- Downloaded Austin Animal Center Intakes (156,287 records)
- Engineered 26 features across 5 feature engineering steps
- Built consolidated table (172,338 records after matching)
- All data quality checks passed

**Phase 2: Star Schema Design & Build (COMPLETE)**
- Designed Kimball conformed star schema
- Built 5 dimensions (4,233 + 16,414 + 20 + 215 + 76 = 20,958 rows)
- Built fact table (172,044 rows after P99.9 filtering)
- Validated all 7 foreign keys (0 violations)
- Verified grain: one row per animal outcome event
- Applied all dimension completeness principles

**Phase 3: Ground Truth Test Case Generation (COMPLETE)**
- Created 11 comprehensive test cases
- Generated 245 total expected result rows
- **Q11 Complete Redesign:** Changed from reproductive_status to age_group spay/neuter analysis
  - Old: Average age by reproductive status
  - New: Spay/neuter percentages by age group (all 4 age groups)
- Fixed DIM_SEX_ON_OUTCOME to include all age group combinations
- All test cases validated against schema
- Results stored in agent_ground_truth_test_cases.json

### 🔄 Current Phase: Agent Validation

**Phase 4: MindsDB Integration (IN PROGRESS)**
- Set up MindsDB with DuckDB connection
- Register star schema tables
- Execute all test queries
- Prepare for agent validation

**Phase 5: Agent Validation (PENDING)**
- Create validation framework (test_validate_mindsdb_agent_v2.ipynb)
- Run 20 iterations per test case (220 total agent attempts)
- Compare agent-generated SQL to ground truth
- Calculate accuracy metrics:
  - Exact match (generated SQL = ground truth)
  - Semantic equivalence (same results, different SQL)
  - Result accuracy (correct output)
- Success criteria: >80% accuracy on test cases

---

## Dataset Overview

**Name:** Austin Animal Center Outcomes & Intakes  
**Source:** City of Austin Open Data Portal  
**Format:** CSV (manual download)  
**Outcomes:** 173,775 records (Oct 1, 2013 - May 5, 2025)  
**Intakes:** 156,287 records (Oct 1, 2013 - May 5, 2025)  
**Star Schema Fact Records:** 172,044 (after intake-outcome matching + P99.9 filtering)  

**Important Limitation:**
> This dataset contains **historical outcomes**, not current shelter inventory. The agent helps users understand patterns and trends — it does NOT show which animals are currently available for adoption.

---

## Analytical Grain

**Fact Grain:** One row per animal outcome event  
**Business Definition:** Each time an animal is released from the shelter  
**Uniqueness Key:** (animal_id, outcome_datetime)  
**Why This Grain:** Non-negotiable; drives all modeling decisions

---

## Star Schema Architecture

### Fact Table: FACT_ANIMAL_OUTCOME

**Row Count:** 172,044 (one per outcome event)  
**Surrogate Key:** fact_id  
**Foreign Keys:** 7 (all with 0 violations)
- animal_attributes_key (→ dim_animal_attributes)
- sex_key (→ dim_sex_on_outcome)
- outcome_date_key (→ dim_date)
- intake_date_key (→ dim_date)
- outcome_key (→ dim_outcome_type)
- intake_details_key (→ dim_intake_details)

**Degenerate Dimensions:** animal_id (individual animal drill-down)  
**Additive Measures:**
- days_in_shelter
- age_at_outcome_days
- age_at_outcome_years

### Dimensions

| Dimension | Rows | Purpose |
|-----------|------|---------|
| **dim_date** | 4,233 | Calendar (Oct 1, 2013 - May 5, 2025); role-plays outcome + intake dates |
| **dim_animal_attributes** | 16,414 | Animal type, breed, color combinations |
| **dim_sex_on_outcome** | 20 | Sex, reproductive status, + age group (✅ FIXED - all age groups) |
| **dim_outcome_type** | 215 | Outcome types + subtypes + stay duration |
| **dim_intake_details** | 76 | Intake types + conditions + severity |

---

## Ground Truth Test Cases

### Test Suite Overview
- **Total Tests:** 11
- **Total Expected Rows:** 245
- **Coverage:** Business questions across outcomes, breeds, conditions, trends, demographics
- **Status:** ✅ All tests validated against star schema

### Key Test Case: Q11 (Redesigned)
**Title:** Reproductive Status by Age Group  
**Question:** "By age group, what percentage of animals are spayed/neutered vs intact?"

**Ground Truth SQL:**
```sql
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
ORDER BY CASE 
  WHEN s.age_group = 'Under 1 Year' THEN 1
  WHEN s.age_group = '1-5 Years' THEN 2
  WHEN s.age_group = '5-10 Years' THEN 3
  WHEN s.age_group = 'Over 10 Years' THEN 4
  ELSE 5 END
```

**Expected Results (4 rows):**
| Age Group | Total Animals | Intact % | Spayed/Neutered % |
|-----------|---------------|----------|-------------------|
| Under 1 Year | 77,602 | 31.0% | 69.0% |
| 1-5 Years | 71,733 | 22.1% | 77.9% |
| 5-10 Years | 16,148 | 15.3% | 84.7% |
| Over 10 Years | 6,561 | 19.7% | 80.3% |

**Key Insight:** Spay/neuter rates increase with age (younger animals are less likely to be sterilized), suggesting adoption requirements or shelter processing time.

### Other Test Cases (Summary)

1. **Q1 - Outcome Distribution** (12 rows): Overall outcome type distribution
2. **Q2 - Top Breed Groups** (7 rows): Most common breeds
3. **Q3 - Adoption Success Rate** (5 rows): Highest adoption rate breeds
4. **Q4 - High Demand Animals** (5 rows): Shortest stays before adoption
5. **Q5 - High Need Animals** (10 rows): Longest stays (breed + condition)
6. **Q6 - Sick & Injured Outcomes** (39 rows): Health condition outcomes
7. **Q7 - Stay Duration by Outcome** (43 rows): Length of stay distribution
8. **Q8 - Monthly Trends 2016** (82 rows): Seasonal patterns
9. **Q9 - Gender Distribution** (34 rows): Gender outcome differences
10. **Q10 - Intake Type Analysis** (6 rows): Intake method effectiveness

---

## Technology Stack

### Storage & Modeling
- **DuckDB (local)** — No server, no credentials, excellent dimensional modeling support
  - Database file: `animal_shelter.duckdb`
  - All tables persisted (dimensions + fact + consolidated table for reference)

### Data Agent Layer
- **MindsDB (open-source)** — Bridges natural language to SQL
  - Registers DuckDB as data source
  - Learns schema from documentation
  - Generates SQL from user questions

### Development & Documentation
- **Jupyter Notebooks** — Interactive development and validation
  - `consolidate_features_into_single_table.ipynb` — Feature engineering
  - `build_star_schema_tables.ipynb` — Dimension + fact table build
  - `setup_mindsdb_integration.ipynb` — MindsDB setup (test queries fixed)
  - `test_validate_mindsdb_agent.ipynb` — Agent validation framework

- **Python Scripts** — Standalone utilities
  - `generate_test_cases.py` — Generate ground truth test cases (all 11 tests)
  - `clean_null_outcomes.py` — Data cleaning utility

- **Markdown Documentation**
  - `PROJECT_WORKFLOW.md` — End-to-end project status (updated)
  - `STAR_SCHEMA_DESIGN.md` — Dimensional model specification (updated)
  - `DataAgent_Refined.md` — This file (agent instructions & architecture)
  - `SCHEMA_AUDIT_RESULTS.md` — Validation report
  - `MINDSDB_SCHEMA_CONTEXT.txt` — Schema context for agent
  - `mindsdb_config.json` — MindsDB configuration

---

## Workflow

### ✅ Completed Workflow Steps

**Step 1 — Acquire Data** ✅
- Downloaded Austin Animal Outcomes CSV (173,775 records)
- Downloaded Austin Animal Intakes CSV (156,287 records)
- Verified data integrity and row counts

**Step 2 — Load & Engineer** ✅
- Loaded raw data into DuckDB
- Built consolidated table with all 26 engineered features
- 172,338 records with proper intake-outcome matching

**Step 3 — Build Star Schema** ✅
- Created 5 dimensions with proper grain
- Built fact table (172,044 rows)
- Validated all foreign keys (0 violations)

**Step 4 — Generate Ground Truth** ✅
- Created 11 test cases with expected results
- Fixed Q11 to include all age groups
- Fixed DIM_SEX_ON_OUTCOME to be complete
- Saved all results to JSON file

### 🔄 Current Workflow Steps (Next)

**Step 5 — Setup MindsDB** 🔄
```bash
# Run this notebook to register schema with MindsDB
jupyter notebook setup_mindsdb_integration.ipynb
```

**Step 6 — Validate Agent** ⏳
```bash
# Create and run agent validation
jupyter notebook test_validate_mindsdb_agent_v2.ipynb
```

**Step 7 — Deploy (Optional)** ⏳
- Package for sharing
- Build BI dashboard (optional)
- Deploy to cloud (optional)

---

## Agent Capabilities & Limitations

### ✅ Agent CAN Do

**Help at-risk animals:**
- "Which breeds tend to stay the longest?"
- "What percentage of senior dogs have live outcomes vs puppies?"
- "Are cats or dogs more likely to be euthanized?"
- "What intake conditions are associated with longer stays?"

**Find high-demand pets:**
- "Which breeds get adopted fastest?"
- "How quickly do golden retrievers get adopted?"
- "What types of puppies have the shortest stays?"

**Understand trends:**
- "How have outcomes changed year-over-year?"
- "Do outcomes differ between weekdays and weekends?"
- "What's the adoption rate for dogs vs cats?"

### ❌ Agent CANNOT Do

- Show **current shelter inventory** (historical data only)
- Predict **future outcomes** for specific animals
- Access **real-time availability**
- Provide **medical advice**
- Make **adoption recommendations** (only facts)

**Key message to users:**
> "This tool shows **historical patterns** from 2013-2025. Use these insights when visiting the shelter or checking their website for current availability."

---

## Guiding Principles

✅ **Optimize for clarity**, not enterprise scale  
✅ **SQL-first** (classic Kimball)  
✅ **Minimal setup**, minimal accounts  
✅ Everything runs **locally**  
✅ **LLM as pair programmer**, not architect  
✅ **User-facing insights**, not technical queries  
✅ **Test-driven** (ground truth test cases first)  
✅ **Reproducible** (schema rebuilt from scripts)  

---

## Success Criteria (Current Status)

- ✅ Dimensional model matches Kimball principles
- ✅ Queries are intuitive and business-readable
- ⏳ Agent answers trend-based questions correctly (validating next)
- ⏳ Agent gracefully handles out-of-scope questions
- ✅ Entire project can be shared or demoed
- ✅ Non-technical user can understand agent's purpose and limitations

---

## Deliverables Checklist

- ✅ DuckDB database with star schema (animal_shelter.duckdb)
- ✅ Consolidated table with engineered features (172,338 rows)
- ✅ Dimensional model documentation (STAR_SCHEMA_DESIGN.md)
- ✅ Feature engineering notebook (consolidate_features_into_single_table.ipynb)
- ✅ Star schema build notebook (build_star_schema_tables.ipynb) — 25 cells
- ✅ Ground truth test cases (agent_ground_truth_test_cases.json) — 11 tests, 245 rows
- ✅ Test case generation script (generate_test_cases.py) — all 11 tests
- ✅ Schema audit report (SCHEMA_AUDIT_RESULTS.md)
- ✅ Agent instructions (DataAgent_Refined.md)
- ✅ Project workflow (PROJECT_WORKFLOW.md)
- ✅ MindsDB configuration (mindsdb_config.json)
- ✅ Schema context for agent (MINDSDB_SCHEMA_CONTEXT.txt)
- ⏳ MindsDB setup notebook (setup_mindsdb_integration.ipynb — ready to run)
- ⏳ Agent validation notebook (test_validate_mindsdb_agent_v2.ipynb — ready to create)
- ⏳ User README (future)

---

## Notes

- **Reproducible:** All code is version-controlled and can be re-executed
- **Scalable:** Skills transfer directly to Fabric, Snowflake, Databricks
- **Educational:** Demonstrates professional dimensional modeling practices
- **Complete:** From raw data to validated agent in one cohesive project

---

## Limitations & Disclaimers

- Data reflects **historical outcomes only** — not current availability
- Patterns may vary by shelter, region, and time period
- This tool is for educational and informational purposes only
- Always verify information with shelter staff before making adoption decisions
- Agent limitations documented in "Agent Capabilities & Limitations" section above
