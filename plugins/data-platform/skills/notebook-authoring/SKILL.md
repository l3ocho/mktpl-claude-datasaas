---
name: notebook-authoring
description: Jupyter notebook cell patterns, structure, and documentation standards for analytical notebooks
---

# Notebook Authoring

## Purpose

Defines cell structure, documentation patterns, and output management for Jupyter notebooks produced during data exploration. Load this skill when generating `.ipynb` files.

---

## Cell Cycle Pattern (MANDATORY)

Every analytical unit follows this four-cell cycle:

```
[1. Context Cell — Markdown]    What we're about to do and why
[2. Code Cell]                  The actual computation / query
[3. Interpretation Cell — Markdown]  What the visualization shows, metric definitions, what to look for
[4. Visualization Cell]         The chart / figure output
```

### Cell 1: Context Cell

One to three sentences. Answers: "What is this code block doing and why does it matter for our analysis?"

**Good:** "Query median household income by neighbourhood for 2021, then compute income quintiles. This segmentation will be used throughout the analysis to compare neighbourhood groups."

**Bad:** "Load data." (Too vague — no analytical context.)

### Cell 3: Interpretation Cell

This is the most important cell. It appears BEFORE the visualization and prepares the reader.

**Required sections:**

- **Title** — analytical, descriptive (e.g., `### Income Distribution Reveals Bimodal Pattern`)
- **What this shows** — one sentence on the chart's purpose
- **Measure definitions** — define every metric on the chart. Never assume the reader knows what "Shannon Diversity Index" or "CPI-adjusted" means
- **What to look for** — guide the reader's eye. "Notice the gap between quintile 3 and 4" or "The cluster in the southeast corner contains all high-density neighbourhoods"
- **Methodology notes** — if any (CPI adjustment, imputation handling, outlier exclusion)

### Between-Section Transitions

When moving between analytical themes, add a transition markdown cell:

```markdown
---

## Part 2: Spatial Patterns

The income analysis above revealed two distinct neighbourhood clusters.
Now we examine whether these clusters have geographic coherence —
do wealthy and poor neighbourhoods form contiguous spatial regions,
or are they distributed randomly across Toronto?
```

---

## Notebook Structure

### First Cell: Environment Setup

```python
import os
import warnings
warnings.filterwarnings('ignore')

# Database connection — replace with dotenv before delivery
os.environ['DATABASE_URL'] = '<connection_string>'

import pandas as pd
import numpy as np
from scipy import stats
from sqlalchemy import create_engine
import plotly.graph_objects as go

engine = create_engine(os.environ.get('DATABASE_URL'))
```

### Second Cell: Layout Template

Load the design system template (from `notebook-design-system` skill if available):

```python
LAYOUT_TEMPLATE = dict(
    # ... design system values
)

def apply_layout(fig, title, **overrides):
    """Apply standard layout to any figure."""
    layout = {**LAYOUT_TEMPLATE, 'title': dict(text=title, **LAYOUT_TEMPLATE.get('title', {}))}
    layout.update(overrides)
    fig.update_layout(**layout)
    return fig
```

### Third Cell: Measure Tree / Schema Reference

Output the schema discovery results from Phase 1 of `data-exploration-workflow`. This cell serves as a reference table for the rest of the notebook.

### Remaining Cells: Follow the Cell Cycle Pattern

---

## Pre-Delivery Cleanup

Before declaring notebooks complete:

1. **Replace connection strings** — every notebook's setup cell must use `dotenv`:
   ```python
   import os
   from dotenv import load_dotenv
   load_dotenv()
   engine = create_engine(os.environ.get('DATABASE_URL'))
   ```

2. **Clear cell outputs if sensitive** — no query results containing PII or credentials in saved outputs

3. **Verify execution order** — every notebook must execute top-to-bottom with zero errors via:
   ```bash
   jupyter nbconvert --to notebook --execute notebook.ipynb --output notebook.ipynb
   ```

4. **Check markdown rendering** — all markdown cells render correctly (no broken links, no raw HTML artifacts)

---

## Notebook Naming

Use descriptive names that reflect analytical theme, not ordinal numbers:

| Good | Bad |
|---|---|
| `schema_discovery.ipynb` | `01_data.ipynb` |
| `income_inequality_analysis.ipynb` | `02_demographics.ipynb` |
| `spatial_clustering.ipynb` | `03_maps.ipynb` |
| `cross_dimensional_synthesis.ipynb` | `05_final.ipynb` |

Ordinal prefixes (01_, 02_) are acceptable ONLY for suggested reading order, but the name after the prefix must be descriptive.
