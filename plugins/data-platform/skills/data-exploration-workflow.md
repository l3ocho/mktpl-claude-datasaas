---
name: data-exploration-workflow
description: Five-phase autonomous exploratory data analysis methodology for Jupyter notebooks
---

# Data Exploration Workflow

## Purpose

Guides autonomous exploratory data analysis from raw schema to non-obvious insights. This is NOT a profiling workflow — profiling is Phase 2. This skill encodes the full analytical thinking process: discover → profile → hypothesize → test → synthesize.

Load this skill when performing open-ended data exploration, Jupyter notebook generation, or any task where the goal is "find what's interesting in this data" rather than "validate this data."

---

## Phase 1: Schema Discovery & Measure Classification

**Goal:** Build a complete map of the data landscape before touching any values.

### Steps

1. **Enumerate all tables** in the target schema using `pg_tables`
2. **Get full column metadata** for every table using `pg_columns`
3. **Classify each column** into one of:

| Classification | Definition | Examples |
|---|---|---|
| **Dimension — Categorical** | Finite set of labels, used for grouping/filtering | neighbourhood_name, category, census_year |
| **Dimension — Hierarchical** | Categorical with parent-child relationships | category → subcategory, province → city → neighbourhood |
| **Dimension — Geographic** | Spatial or location identifiers | geometry, latitude, longitude, postal_code |
| **Dimension — Temporal** | Time-based for trend analysis | census_year, created_at, period |
| **Measure — Additive** | Numeric, meaningful when summed across dimensions | population, total_income, dwelling_count |
| **Measure — Semi-Additive** | Numeric, summable across some dimensions only | account_balance (sum across accounts, not time) |
| **Measure — Non-Additive** | Numeric, never meaningful when summed | median_income, diversity_index, percentage, rate |
| **Identifier** | Primary/foreign keys, join columns | neighbourhood_id, profile_id |
| **Metadata** | Data quality flags, system columns | is_imputed, is_suppressed, updated_at |

4. **Identify join paths** between tables (FK relationships, shared dimension keys)
5. **Identify natural hierarchies** (columns that form drill-down paths)
6. **Document the full measure tree** in a markdown cell as the first output

### Output

A reference table showing:
- Every table with row counts
- Every column with classification, data type, null rate, distinct count
- Join graph between tables
- Hierarchy trees (e.g., category → subcategory with counts)

---

## Phase 2: Statistical Profiling (Beyond Basics)

**Goal:** Go deeper than null counts and means. Understand the shape of every distribution.

### For Every Numeric Measure

| Metric | Why It Matters |
|---|---|
| Mean, median, mode | Central tendency — if mean ≠ median, distribution is skewed |
| Std dev, IQR | Spread — high IQR relative to median = high variability |
| Skewness | > 0.5 or < -0.5 = meaningfully skewed, investigate why |
| Kurtosis | > 3 = heavy tails (outliers), < 3 = light tails |
| Min, Max, Range | Sanity check — are extremes plausible? |
| Percentiles (5th, 25th, 50th, 75th, 95th) | Distribution shape without assumptions |

### For Every Categorical Dimension

| Metric | Why It Matters |
|---|---|
| Cardinality (distinct count) | Low = good for grouping, high = may need binning |
| Top 5 / Bottom 5 values by frequency | Dominant vs. rare categories |
| Shannon entropy | Distribution evenness — low entropy = dominated by few values |
| Null rate | Missing category data needs investigation |

### For Temporal Dimensions

| Metric | Why It Matters |
|---|---|
| Distinct periods | How many time points exist |
| Coverage gaps | Missing periods in the sequence |
| Entity coverage per period | Do all entities appear in all periods? |

### Cross-Column Checks

| Check | Why It Matters |
|---|---|
| **Correlation matrix** (all numeric pairs) | Identify strongly correlated variables (r > 0.7 or r < -0.7) |
| **Multicollinearity scan** | Variables that are near-linear combinations of others — affects interpretation |
| **Simpson's paradox check** | Does a trend reverse when you control for a third variable? Test top correlations against key dimensions |

---

## Phase 3: Hypothesis Generation

**Goal:** Turn profiling observations into testable questions. This is where analysis becomes interesting.

### Hypothesis Generation Rules

1. **Every surprising statistic generates a hypothesis.** If skewness > 1.0 for income, ask: "Is this a bimodal distribution with two distinct neighbourhood clusters?"
2. **Every strong correlation generates a hypothesis.** If income correlates with education at r=0.8, ask: "Does this hold across all geographic regions, or is it driven by a few wealthy suburbs?"
3. **Every outlier generates a hypothesis.** If one neighbourhood has 3x the population density, ask: "Is this real density or a data artifact from small land area?"
4. **Every temporal change generates a hypothesis.** If diversity index increased from 2016→2021, ask: "Did all neighbourhoods diversify equally, or did a few neighbourhoods drive the aggregate?"
5. **Generate at least 10 hypotheses.** Rank them by: (a) testability with available data, (b) potential surprise value, (c) practical relevance.
6. **Select top 5-7 for testing.** Document the rest as "future investigation" in a markdown cell.

### Hypothesis Format

For each hypothesis, document:
- **H:** One-sentence statement (e.g., "Neighbourhoods in the top income quintile cluster geographically in the north-central corridor")
- **Test:** What analysis would confirm or refute it (e.g., "Choropleth map of income quintiles + spatial autocorrelation test")
- **Data needed:** Which tables, columns, joins, filters
- **Expected insight if confirmed:** Why this matters

---

## Phase 4: Hypothesis Testing & Deep Dives

**Goal:** For each selected hypothesis, run the analysis, interpret the results, and follow interesting threads.

### Testing Protocol

For each hypothesis:

1. **Query the data** — write the SQL or pandas operation needed
2. **Choose the right visualization** — load `analytical-chart-selection` skill for guidance
3. **Run a statistical test where appropriate:**

| Question Type | Statistical Test | scipy Function |
|---|---|---|
| Is this distribution normal? | Shapiro-Wilk (n < 5000) or D'Agostino-Pearson | `scipy.stats.shapiro`, `scipy.stats.normaltest` |
| Are these two groups different? | Mann-Whitney U (non-normal) or independent t-test | `scipy.stats.mannwhitneyu`, `scipy.stats.ttest_ind` |
| Did this metric change 2016→2021? | Wilcoxon signed-rank (paired, non-normal) or paired t-test | `scipy.stats.wilcoxon`, `scipy.stats.ttest_rel` |
| Are these variables related? | Spearman rank correlation (non-normal) or Pearson | `scipy.stats.spearmanr`, `scipy.stats.pearsonr` |
| Does group membership predict a metric? | Kruskal-Wallis (3+ groups, non-normal) or ANOVA | `scipy.stats.kruskal`, `scipy.stats.f_oneway` |
| Is there spatial clustering? | Moran's I (if spatial weights available) or visual clustering | Manual or `pysal` if available |

4. **Interpret the result** — in a markdown cell, state:
   - Whether the hypothesis is confirmed, refuted, or inconclusive
   - The effect size (not just p-value — statistical significance ≠ practical significance)
   - What follow-up question this raises
5. **Follow the thread** — if results suggest a deeper pattern, pursue it. Don't stop at the first chart.

### Depth Indicators

A hypothesis is "deep enough" when:
- You can explain the **mechanism** (why does this pattern exist?), or
- You've eliminated the obvious confounders, or
- You've found the **boundary condition** (the pattern holds for X but breaks for Y)

A hypothesis is NOT deep enough when:
- You showed one chart and moved on
- You reported a correlation without checking if it's driven by outliers or a third variable
- You described what the chart shows without interpreting what it means

---

## Phase 5: Narrative Synthesis

**Goal:** Rank and present findings as a coherent analytical story.

### Ranking Criteria

For each finding, score on three dimensions:

| Dimension | Low (1) | Medium (3) | High (5) |
|---|---|---|---|
| **Surprise** | Expected from common knowledge | Somewhat unexpected | Genuinely counterintuitive |
| **Effect Size** | Trivial difference | Moderate, noticeable | Large, consequential |
| **Actionability** | Pure trivia | Informs understanding | Could drive decisions |

**Composite score = Surprise × Effect × Actionability.** Findings scoring ≥ 27 (3×3×3) are "non-obvious insights."

### Synthesis Structure

1. **Executive Summary** — 3-5 bullet points, plain language, no jargon
2. **Top Findings** — each with: the insight, the evidence (chart + stat test), the implication
3. **Patterns Across Dimensions** — what themes connect multiple findings?
4. **Limitations & Caveats** — what can't this data tell us? What assumptions did we make?
5. **Questions for Further Investigation** — the hypotheses we didn't get to, or new ones that emerged

---

## Anti-Patterns (What NOT to Do)

| Anti-Pattern | Why It Fails | Do This Instead |
|---|---|---|
| Chart spam — 30 visualizations with no narrative | Reader can't find the signal in the noise | Fewer charts, more interpretation between them |
| Describing charts instead of interpreting them | "This shows income by neighbourhood" is not analysis | "The bimodal income distribution suggests two distinct neighbourhood archetypes..." |
| Only testing obvious hypotheses | "Rich neighbourhoods have higher education" — no surprise value | Test the non-obvious: "Do high-diversity neighbourhoods have *lower* income inequality?" |
| Stopping at correlation | "Income and education are correlated" — so what? | "The correlation breaks down in the northwest cluster, suggesting a confounding geographic factor" |
| Using exotic chart types for their own sake | Sankey diagram of obvious relationships wastes attention | Use the simplest chart that reveals the pattern; upgrade only if complexity adds insight |
| Treating p < 0.05 as the finish line | Statistical significance without practical significance is meaningless | Always report effect size alongside p-value |
