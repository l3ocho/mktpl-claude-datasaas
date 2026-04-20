# Visual Header

## Standard Format

Display at the start of every command execution:

```
+----------------------------------------------------------------------+
|  DATA-PLATFORM - [Command Name]                                      |
+----------------------------------------------------------------------+
```

## Command Headers

| Command | Header Text |
|---------|-------------|
| data-setup | Setup Wizard |
| data-ingest | Ingest |
| data-profile | Data Profile |
| data-schema | Schema Explorer |
| data-quality | Data Quality |
| data-run | dbt Run |
| dbt-test | dbt Tests |
| data-lineage | Lineage |
| lineage-viz | Lineage Visualization |
| data-explain | Model Explanation |
| data-review | Data Review |
| data-gate | Data Gate |

## Summary Box Format

For completion summaries:

```
+============================================================+
|            DATA-PLATFORM [OPERATION] COMPLETE              |
+============================================================+
| Component:         [Status]                                |
| Component:         [Status]                                |
+============================================================+
```

## Status Indicators

- Success: `[check]` or `Ready`
- Warning: `[!]` or `Partial`
- Failure: `[X]` or `Failed`
