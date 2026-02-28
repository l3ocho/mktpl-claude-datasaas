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

### Mandatory Coverage Requirements

The selected hypotheses (the 5-7 that pass the Quality Gate and proceed to Phase 4) must collectively satisfy ALL of the following coverage requirements. If they don't, generate additional hypotheses until coverage is met.

#### Requirement 1: Table Coverage
Hypotheses must draw data from **at least 3 different mart tables** (not counting the geometry table which is just a join target). If all hypotheses can be answered from a single table, the analysis is too narrow.

#### Requirement 2: Temporal Coverage
If the schema contains multiple time periods (e.g., census years, yearly data), **at least 1 hypothesis must involve a temporal comparison** — how did something change between periods? Temporal shifts are where the most interesting findings live because they reveal dynamics, not just static snapshots.

#### Requirement 3: Spatial Coverage
If geometry data is available (PostGIS columns, lat/lon, boundary polygons), **at least 1 hypothesis must involve spatial analysis** — do patterns cluster geographically? Is there spatial autocorrelation? Do findings hold across all areas or only in specific regions? Spatial patterns are invisible in tabular analysis and frequently reveal non-obvious structure.

#### Requirement 4: Depth Coverage
**At least 2 hypotheses must involve joining across tables** — combining data from different domains (e.g., demographics + safety, housing + amenities, profile categories + income). Single-table analysis can only find relationships the table was designed to show. Cross-table analysis finds relationships nobody planned for.

#### Coverage Check Format

Before proceeding to the Hypothesis Quality Gate, verify coverage:

```
COVERAGE CHECK
━━━━━━━━━━━━━━
Tables used: foundation, safety, housing, amenities, profile (5/9) ✅ ≥3
Temporal:    H4 compares 2016→2021 crime trends ✅
Spatial:     H7 tests geographic clustering of income-crime residuals ✅
Cross-table: H3 joins housing + demographics, H6 joins profile + foundation ✅ ≥2

Coverage: PASS
```

If any requirement is not met:
```
COVERAGE CHECK
━━━━━━━━━━━━━━
Tables used: foundation, overview (2/9) ❌ Need ≥3
Temporal:    None ❌ Need ≥1
Spatial:     None ❌ Need ≥1
Cross-table: None ❌ Need ≥2

Coverage: FAIL — Generate additional hypotheses targeting missing requirements
```
```

### Hypothesis Format

For each hypothesis, document:
- **H:** One-sentence statement (e.g., "Neighbourhoods in the top income quintile cluster geographically in the north-central corridor")
- **Test:** What analysis would confirm or refute it (e.g., "Choropleth map of income quintiles + spatial autocorrelation test")
- **Data needed:** Which tables, columns, joins, filters
- **Expected insight if confirmed:** Why this matters

---

### Mandatory Coverage Requirements

To ensure the hypothesis set isn't accidentally biased toward shallow analysis, every selected set of 5-7 hypotheses must meet these four diversity rules. Check them BEFORE committing to Phase 4 testing.

#### Requirement 1: Table Coverage
Hypotheses must touch at least 3 different tables. This prevents analyzing one table in isolation and forces cross-table insight discovery.

#### Requirement 2: Measure Type Coverage
Hypotheses must include:
- At least 1 testing an **additive measure** (e.g., population, total_income, count)
- At least 1 testing a **non-additive measure** (e.g., median_income, diversity_index, rate)
- At least 1 testing a **categorical dimension** (e.g., whether neighbourhoods cluster by type)

#### Requirement 3: Dimension Type Coverage
Hypotheses must include:
- At least 1 using a **temporal dimension** (e.g., testing 2016→2021 change)
- At least 1 using a **geographic dimension** (e.g., spatial clustering)
- At least 1 using a **hierarchical categorical** (e.g., category → subcategory breakdown)

#### Requirement 4: Depth Coverage
Hypotheses must include:
- At least 1 **univariate insight** (e.g., "Income distribution in Toronto is bimodal")
- At least 1 **bivariate relationship** (e.g., "Transit commuting predicts median income")
- At least 1 **multivariate or confounder-control hypothesis** (e.g., "Does the income-education relationship persist after controlling for immigration?")

#### Requirement 5: High-Cardinality Table Coverage
If the schema contains a table with **significantly more rows than others** (10x+ the base grain), at least 1 hypothesis must use that table. High-cardinality tables contain the most granular, most unique data in the schema — they exist because someone invested effort to model detailed breakdowns. Ignoring them means ignoring the richest analytical resource.

Examples of high-cardinality tables:
- A profile/survey table with categorical breakdowns (e.g., 108K rows across 22 categories vs. 158 base neighbourhoods)
- A transaction-level table vs. aggregated summaries
- A time-series at daily grain vs. annual summaries

The hypothesis using this table should exploit its unique structure — hierarchical categories, subcategory distributions, cross-category patterns — not just aggregate it back to the base grain.

#### Coverage Check Format

After selecting your 5-7 hypotheses, fill in this coverage matrix:

**PASS example:**
```
Tables:      H1 uses housing, H2 uses foundation, H3 uses housing + demographics ✅ ≥3
Measures:    H1 uses population (additive), H4 uses diversity_index (non-additive), H5 uses neighbourhood_type (categorical) ✅
Dimensions:  H2 tests 2016→2021 change (temporal), H3 tests geographic clustering, H6 uses category hierarchy ✅
Depth:       H1 univariate, H3 bivariate (housing→income), H6 multivariate (income→education controlling for immigration) ✅
High-card:   H8 uses profile table (108K rows, 22 categories) ✅

Coverage: PASS
```

**FAIL example:**
```
Tables:      H1 uses housing, H2 uses housing, H3 uses housing ❌ Need ≥3
Measures:    H1 uses population (additive), H2 uses population (additive), H3 uses population ❌ Need non-additive + categorical
Dimensions:  H1 tests temporal change, H2 tests temporal change ❌ Need geographic + hierarchical
Depth:       All bivariate, no univariate, no multivariate ❌ Need all three types
High-card:   None ❌ Profile table (108K rows) not used

Coverage: FAIL — Generate additional hypotheses targeting missing requirements
```

---

### Hypothesis Quality Gate (MANDATORY before Phase 4)

Before testing ANY hypothesis, pass it through all three filters. If it fails any filter, discard it and generate a replacement. Do NOT proceed to Phase 4 with a hypothesis that fails these checks.

#### Filter 1: Falsifiability

Ask: "What specific data result would make me REJECT this hypothesis?"

If you cannot name a concrete result that would refute it, the hypothesis is unfalsifiable and must be discarded.

- ✅ PASS: "Neighbourhoods with >50% transit commuting have crime rates at least 20% lower than those with <20% transit commuting" — refutable if the difference is <20% or reversed
- ❌ FAIL: "Income relates to education" — some relationship always exists; this can never be refuted
- ❌ FAIL: "There is variation in housing affordability" — trivially true for any dataset with variance

#### Filter 2: Circularity Check

Ask: "Is my independent variable a component, input, or derivative of my dependent variable?"

If variable A was used to compute variable B, correlating A with B is arithmetic, not analysis. Check how composite scores and indices were built before testing them against their own inputs.

- ✅ PASS: "Transit commuting % predicts median household income" — income is not computed from transit data
- ❌ FAIL: "Transit commuting % predicts livability_score" — if livability_score includes amenity_score which includes transit-adjacent metrics, this is circular
- ❌ FAIL: "diversity_index correlates with pct_visible_minority" — if diversity_index is Shannon entropy computed over visible minority categories, this is definitional

**How to check:** Before testing any hypothesis involving a composite score or index, query the database or documentation to understand exactly how that score is computed. List its components. If your independent variable appears in that list (directly or through a sub-score), the hypothesis is circular.

#### Filter 3: Novelty Screen

Ask: "Would a second-year undergraduate in this domain already know this?"

If the answer is yes, the hypothesis has zero surprise value and should be replaced with something deeper.

- ✅ PASS: "Neighbourhoods where >30% of residents moved from another city in the last 5 years have LOWER income inequality than stable neighbourhoods" — non-obvious, requires data to verify
- ❌ FAIL: "Wealthier neighbourhoods have higher education levels" — textbook knowledge since forever
- ❌ FAIL: "Population density correlates with transit usage" — obvious by definition in urban planning

**Automatic Novelty Failures — Structural Rule:**

Any hypothesis that is a simple bivariate correlation between two standard socioeconomic indicators WITHOUT at least one of the following modifiers automatically fails the novelty screen:

Standard socioeconomic indicators (the "obvious variables"): income, education, unemployment, crime rate, population density, age, housing cost, home ownership rate, immigration rate.

A hypothesis using two of these variables fails UNLESS it includes at least one of:
- **A moderating variable:** "Does X→Y hold when controlling for Z?"
- **A subgroup condition:** "Does X→Y reverse for neighbourhoods in the top quintile of Z?"
- **A temporal comparison:** "Did the X→Y relationship strengthen or weaken from 2016 to 2021?"
- **An interaction effect:** "Does X→Y depend on the level of Z?"
- **A spatial pattern:** "Does X→Y cluster geographically, or is it spatially random?"
- **A threshold/nonlinearity:** "Is there a tipping point in X beyond which Y changes sharply?"

Examples:
- ❌ FAIL: "Education correlates with income" — two obvious variables, no modifier
- ❌ FAIL: "Unemployment correlates with crime rate" — two obvious variables, no modifier
- ❌ FAIL: "Population density relates to housing cost" — two obvious variables, no modifier
- ✅ PASS: "The education→income relationship weakens in neighbourhoods with >40% immigrant population" — modifier: subgroup condition
- ✅ PASS: "Unemployment→crime strengthened from 2016 to 2021 in high-density neighbourhoods but not low-density" — modifier: temporal + interaction
- ✅ PASS: "There is a density threshold (~8,000/km²) above which crime rate drops rather than rises" — modifier: nonlinearity/threshold

**Replacement strategy:** When a hypothesis fails the novelty screen, push it one level deeper. "Wealthy neighbourhoods have higher education" → "Does the income-education relationship break down in neighbourhoods with high immigration rates?" The deeper version tests a boundary condition, which is where non-obvious findings live.

#### Gate Output

After filtering, document which hypotheses were discarded and why. This transparency prevents self-deception. Format:

```
HYPOTHESIS QUALITY GATE
━━━━━━━━━━━━━━━━━━━━━━
Passed (5):
  H1: [statement] — Falsifiable ✓ | Non-circular ✓ | Novel ✓
  H3: [statement] — Falsifiable ✓ | Non-circular ✓ | Novel ✓
  ...

Discarded (5):
  H2: [statement] — FAILED: Circularity (livability_score contains amenity inputs)
  H4: [statement] — FAILED: Novelty (textbook urban planning)
  H6: [statement] — FAILED: Falsifiability (unfalsifiable "X relates to Y")
  ...

Replacements generated (3):
  H2b: [deeper version] — Falsifiable ✓ | Non-circular ✓ | Novel ✓
  ...
```
```

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

4. **Interpret the result** — in a markdown cell, provide ALL of the following. Missing any item means the hypothesis is NOT confirmed.

   **Required for every hypothesis test:**
   - **Verdict:** Confirmed, Refuted, or Inconclusive — with the specific threshold that determined it
   - **Exact statistics:** r = 0.XX, R² = 0.XX, p = X.XXe-XX (no "moderate-to-strong", no ranges like "0.2–0.4")
   - **Effect size interpretation:** Use standard benchmarks:
     - Correlation: |r| < 0.3 = weak, 0.3–0.5 = moderate, > 0.5 = strong
     - R²: < 0.09 = trivial, 0.09–0.25 = small, 0.25–0.49 = moderate, > 0.49 = large
     - Cohen's d: < 0.2 = trivial, 0.2–0.5 = small, 0.5–0.8 = moderate, > 0.8 = large
   - **Practical significance:** Is this effect large enough to matter in the real world? A statistically significant r = 0.15 with p < 0.001 is still a trivial relationship.
   - **At least one confounder checked:** For every confirmed correlation, test whether it survives when controlling for the most obvious third variable (e.g., does income-education correlation hold after controlling for immigration status?)
   - **Null comparison:** What would you expect from random/shuffled data? If your r = 0.25 and shuffled data gives r = 0.15, the signal is marginal.
   - **What follow-up question this raises**

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

### Completion Requirement

Every hypothesis selected for Phase 4 testing must be FULLY tested before proceeding to Phase 5. "Fully tested" means:

- Statistical test executed with exact values (r, R², p, Cohen's d)
- At least one confounder controlled
- Interpretation written with verdict (confirmed/refuted/inconclusive)
- Visualization produced

**If a hypothesis cannot be fully tested** (data unavailable, query too complex, time constraints), it must be explicitly marked as **DROPPED** with a reason, and it must NOT appear in the Phase 5 synthesis or the final report findings table.

Hypotheses with status "PENDING", "PARTIAL", "TBD", or "IN PROGRESS" are not permitted in the final output. Either finish it or drop it.

**Drop format:**
```
DROPPED: H9 — Immigration >40% drives rent inflation
Reason: Rental data granularity insufficient to isolate immigration effect from general market trends
Status: Moved to "Questions for Further Investigation"
```

---

### Self-Critique Gate (MANDATORY before Phase 5)

Before writing the synthesis, review ALL findings and apply these checks. Any finding that fails must be either deepened or demoted to "observation" (not presented as a key finding).

#### Check 1: The "So What?" Test

For each finding, complete this sentence: "A city planner / business analyst / domain expert should change their decision about ______ because of this finding."

If you cannot complete the sentence with something specific, the finding has no practical value.

#### Check 2: The Mechanism Test

For each finding, answer: "WHY does this pattern exist?"

If your answer is "unknown" or "requires further investigation" for every finding, you stopped too early. At least 2 of your top findings must include a tested (not speculated) mechanism — meaning you ran an additional analysis to investigate the why, not just reported the what.

#### Check 3: The Confounder Test

For each confirmed correlation, answer: "Did I check whether a third variable explains this?"

If you confirmed a correlation without controlling for at least one obvious confounder, the finding is unverified. Run the partial correlation or stratified analysis before reporting it.

#### Check 4: The Circular Reasoning Audit

Review every finding that involves a composite score, index, or derived metric. Ask: "Am I reporting that a thing correlates with itself?"

This catches circularity that slipped past the Phase 3 gate (e.g., using a different variable name that's actually derived from the same source).

#### Check 5: The Domain Knowledge Check

For each "non-obvious" finding, search your training knowledge: "Is this already well-established in urban planning / data science / the relevant domain?"

If yes, it is NOT non-obvious. Demote it to "confirmed existing knowledge" and do not present it as a discovery. A genuine non-obvious finding is one where the data contradicts or significantly refines common understanding.

#### Gate Integrity Check (Meta-Gate)

After running Checks 1-5, apply this meta-check on the gate results themselves:

**If ALL findings passed all 5 checks (zero demoted, zero requiring more work), the gate itself has failed.**

A 100% pass rate means the hypotheses were too safe, the checks were applied too leniently, or both. This is the analytical equivalent of a test suite where every test passes on the first run — it means the tests aren't testing hard enough.

**When the meta-gate triggers:**
1. Return to Phase 3
2. Discard the weakest 2 findings (lowest effect size or most obvious)
3. Generate 2 replacement hypotheses that are harder to confirm — specifically:
   - Hypotheses that predict a REVERSAL, THRESHOLD, or INTERACTION (not a main effect)
   - Hypotheses that use tables/columns not yet analyzed
4. Test the replacements through Phase 4
5. Re-run the Self-Critique Gate on the full set (original survivors + replacements)
6. On the second pass, the meta-gate is satisfied if at least 1 finding was demoted or refuted

**This rule exists because:** The second analysis run confirmed 6/6 hypotheses. Every finding was a known socioeconomic relationship. Zero surprises. The skill's anti-pattern table says "Confirming every hypothesis signals weak hypotheses, not strong analysis." The meta-gate enforces this structurally.

#### Gate Output

```
SELF-CRITIQUE GATE
━━━━━━━━━━━━━━━━━━
Findings promoted to Key Findings (X):
  F1: [finding] — So What ✓ | Mechanism ✓ | Confounders ✓ | Non-circular ✓ | Novel ✓
  ...

Findings demoted to Observations (X):
  F3: [finding] — DEMOTED: Failed Domain Knowledge Check (known since Jacobs 1961)
  F5: [finding] — DEMOTED: Failed Mechanism Test (no "why" investigated)
  ...

Findings requiring more work (X):
  F4: [finding] — Needs confounder analysis (income not controlled for)
  ...
```
```

#### Gate Integrity Check (Meta-Gate)

After running Checks 1-5, count the results:

- **Passed:** findings that cleared all 5 checks
- **Demoted:** findings downgraded to observations
- **Refuted:** hypotheses where data contradicted the prediction
- **Incomplete:** hypotheses not fully tested (missing stats, no confounder check, partial data)

**Meta-Gate Rule — zero ambiguity:**

Count = Demoted + Refuted + Incomplete.

- **Count ≥ 1 → Meta-Gate PASSES.** Proceed to Phase 5 synthesis.
- **Count = 0 → Meta-Gate FAILS.** Every single finding passed. This means the hypotheses were too safe. Execute the recovery protocol below.

Do NOT interpret "diverse effect sizes" or "varied results" as satisfying this gate. The ONLY thing that satisfies the meta-gate is at least 1 finding that was demoted, refuted, or incomplete. This is a binary check on a count, not a judgment call.

**Recovery protocol when meta-gate fails:**
1. Return to Phase 3
2. Identify the 2 weakest findings (lowest effect size or highest domain-knowledge overlap)
3. Discard them
4. Generate 2 replacement hypotheses that are structurally harder:
   - Must predict a REVERSAL ("X→Y flips sign when Z is high")
   - Or a THRESHOLD ("X has no effect below value V, strong effect above")
   - Or a TEMPORAL DIVERGENCE ("X→Y was positive in 2016 but negative in 2021")
   - Must use at least 1 table not yet analyzed
5. Test replacements through Phase 4 with full Confirmation Standard
6. Re-run Self-Critique Gate on the combined set
7. Second pass: meta-gate passes if Count ≥ 1 (same rule)
8. If meta-gate fails a second time: proceed anyway but document "META-GATE: FAILED TWICE — hypotheses may be too conservative" as a limitation

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
| Correlating a score with its own components | Definitional relationship, not a finding | Check how composite scores are built; never use a component as the independent variable |
| Reporting "moderate-to-strong" instead of numbers | Hides whether the effect actually matters | Always report exact r, R², p, and Cohen's d with standard benchmark interpretation |
| Presenting domain common knowledge as discovery | Wastes reader's attention on things they already know | Push every "obvious" finding one level deeper to find the boundary condition |
| Confirming every hypothesis | Signals weak hypotheses, not strong analysis | If nothing was refuted, your hypotheses were too soft — generate harder ones |
| Speculating mechanisms without testing them | "Transit probably helps because of walkability" is not analysis | Run the sub-analysis: does the pattern hold when controlling for walkability? |
