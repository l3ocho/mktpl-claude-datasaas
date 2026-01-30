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
| initial-setup | Setup Wizard |
| ingest | Ingest |
| profile | Data Profile |
| schema | Schema Explorer |
| data-quality | Data Quality |
| run | dbt Run |
| dbt-test | dbt Tests |
| lineage | Lineage |
| lineage-viz | Lineage Visualization |
| explain | Model Explanation |

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
