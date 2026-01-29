# AGENTS.md
## Austin Animal Outcomes — Shelter Insights Data Agent

### Purpose
Build a **data agent that helps potential adopters understand shelter outcome trends** — empowering them to save animals at risk of extended stays or euthanasia, and to ask better questions when visiting the shelter.

This project also serves as a hands-on exercise in **Kimball-style dimensional modeling** using a modern, local-first toolchain.

### Who Is This For?
- Potential adopters who want to make an informed, compassionate choice
- People interested in rescuing animals that are statistically at higher risk
- Anyone curious about shelter dynamics before visiting in person

### What the Agent Does
- Answers questions about **historical outcome patterns** (not live inventory)
- Identifies which animal types, breeds, ages, or conditions tend to have longer stays or worse outcomes
- Highlights **high-demand pets** that get adopted quickly — so users know to check the shelter frequently for new arrivals
- Helps users understand what to ask shelter staff (e.g., "Do you have any senior cats that have been here a while?")

---

## Guiding Principles
- Optimize for **speed and clarity**, not enterprise scale
- SQL-first (classic Kimball)
- Minimal setup, minimal accounts
- Everything should run **locally**
- LLM acts as a **pair programmer**, not an architect
- **User-facing insights**, not just technical queries

---

## Dataset

**Name:** Austin Animal Center Outcomes  
**Source:** City of Austin Open Data Portal  
**Format:** CSV (manual download)  

**Why this dataset**
- Event-based (perfect for fact tables)
- Rich descriptive attributes (dimensions)
- Natural feature engineering opportunities
- Well-known, realistic civic dataset

**Important Limitation**
> This dataset contains **historical outcomes**, not current shelter inventory. The agent helps users understand patterns and trends — it does NOT show which animals are currently available for adoption.

---

## Analytical Grain

> **One row per animal outcome event**

This grain is non-negotiable and drives all modeling decisions.

---

## Dimensional Model (Kimball & Ross)

### Fact Table

**fact_animal_outcome**
- `animal_key`
- `date_key`
- `outcome_key`
- `intake_condition_key`
- (optional) `location_key`

**Measures**
- `outcome_count` (always = 1)
- `days_in_shelter`
- `age_days_at_outcome`

---

### Dimensions

#### dim_animal
- `animal_key` (surrogate)
- `animal_id` (natural key)
- `animal_type`
- `primary_breed`
- `secondary_breed`
- `color`
- `sex`
- `sterilized_flag`
- `date_of_birth`
- (optional) SCD Type 2 fields

#### dim_date
- `date_key` (YYYYMMDD)
- `date`
- `year`
- `quarter`
- `month`
- `day_of_week`
- `is_weekend`

#### dim_outcome
- `outcome_type`
- `outcome_subtype`
- `is_live_outcome` (engineered)

#### dim_intake_condition
- `intake_condition`
- `severity_bucket` (engineered)

---

## Engineered Features

- **Age at outcome (days)**
- **Age bucket**
  - Puppy/Kitten
  - Adult
  - Senior
- **Length of stay**
  - Same day
  - < 7 days
  - 7–30 days
  - > 30 days
- **Live vs non-live outcome flag**

All engineered features should be:
- Deterministic
- Business-explainable
- Stored in dimensions when appropriate

---

## Technology Stack (Least Friction Path)

### Storage & Modeling
- **DuckDB (local)**
  - No server
  - No credentials
  - Excellent SQL support
  - Ideal for dimensional modeling

### Data Agent Layer
- **MindsDB (open-source or free tier)**
  - Connects directly to DuckDB
  - Provides natural-language → SQL
  - Acts as the "data agent"

### AI Pair Programmer
- LLM (ChatGPT or equivalent)
  - Writes SQL
  - Helps with transformations
  - Documents schema
  - Reviews modeling decisions

---

## Workflow

### Step 1 — Acquire Data
- Download Austin Animal Outcomes CSV
- Store in project directory

### Step 2 — Load Raw Data
- Load CSV into DuckDB as a staging table
- No transformations yet

### Step 3 — Build Dimensions
- Create surrogate keys
- Deduplicate attributes
- Apply business rules
- Engineer dimension-level features

### Step 4 — Build Fact Table
- Enforce grain (1 row per outcome)
- Join to dimensions
- Compute measures

### Step 5 — Validate Model
- Row counts
- Null checks
- Grain verification
- Sanity queries

### Step 6 — Register with MindsDB
- Connect DuckDB as data source
- Expose star schema
- Provide schema context to agent

### Step 7 — Query via Data Agent
Example questions the agent can answer:

**For users wanting to help at-risk animals:**
- "Which breeds tend to stay in the shelter the longest?"
- "What percentage of senior dogs have live outcomes vs. puppies?"
- "Are cats or dogs more likely to be euthanized?"
- "What intake conditions are associated with longer shelter stays?"
- "Do animals that arrive in poor health have worse outcomes?"
- "What's the average length of stay for pit bull mixes?"

**For users wanting high-demand pets:**
- "Which breeds get adopted the fastest?"
- "How quickly do golden retrievers typically get adopted?"
- "What types of puppies have the shortest shelter stays?"
- "Are kittens adopted faster than adult cats?"

**How Users Can Apply These Insights**
> **Helping at-risk animals:** Visit the shelter and ask:
> - "Do you have any senior dogs that have been here a while?"
> - "Are there any animals with medical conditions that need a home?"
> - "Which pets have been overlooked the longest?"
>
> **Finding high-demand pets:** If you want a pet type that "flies off the shelf":
> - Check the shelter's website or call frequently for new arrivals
> - Ask to be notified when that type of animal comes in
> - Be ready to visit quickly when one becomes available

---

## Human–AI Pair Programming Contract

### Human Responsibilities
- Define grain
- Define business logic
- Decide what belongs in facts vs dimensions
- Validate outputs

### AI Responsibilities
- Generate SQL
- Create date dimension
- Write DDL
- Suggest engineered features
- Document schema

**Explicit Instruction to LLM (Data Agent)**
> "You are a shelter insights assistant. Your purpose is to help potential adopters understand historical trends in animal outcomes at the Austin Animal Center. You can help users in two ways:
> 1. **Find at-risk animals:** Identify which types of animals tend to have longer shelter stays or are at higher risk of euthanasia — so users can prioritize saving them.
> 2. **Find high-demand animals:** Identify which types of animals get adopted very quickly — so users know to check the shelter frequently if they want that type of pet.
>
> You do NOT have access to current shelter inventory. Always clarify this limitation if the user asks about currently available pets. Encourage users to take these insights to the shelter and ask staff directly, or to check frequently for new arrivals if they want a high-demand pet."

**Explicit Instruction to LLM (Pair Programmer)**
> "You are a pair programmer. Do not change the grain. Ask clarifying questions about business rules before writing SQL."

---

## Deliverables

- DuckDB database file with star schema
- Documented dimensional model (facts + dimensions)
- Engineered features with business explanations
- Working MindsDB data agent
- Sample questions and expected answers
- User-facing README explaining what the agent can (and cannot) do

---

## Success Criteria

- Dimensional model matches Kimball principles
- Queries are intuitive and business-readable
- Agent answers trend-based questions correctly
- Agent gracefully handles out-of-scope questions (e.g., "What pets are available now?")
- Entire project can be shared or demoed
- A non-technical user can understand the agent's purpose and limitations

---

## Notes

- This project is intentionally small and complete
- Skills transfer directly to Fabric, Snowflake, Databricks
- Focus is **thinking and modeling**, not platform mastery
- The agent is a **decision-support tool**, not a pet search engine

---

## Limitations & Disclaimers

- Data reflects **historical outcomes only** — not current availability
- Patterns may vary by shelter, region, and time period
- This tool is for educational and informational purposes
- Always verify information with shelter staff before making adoption decisions
