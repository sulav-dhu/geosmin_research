# Input contract and limits

The public modules do not read a laboratory workbook. Callers must prepare their own tables and obtain any necessary permission for the data they use.

## Episode builder

`build_episodes(obs, gap=28, closure=1, start="2016-01-01")` expects a pandas DataFrame sorted by collection date. At minimum, each row represents one observed sampling date for one compound and contains:

| Field | Meaning |
| --- | --- |
| `date` | pandas timestamp of the observation |
| `state` | `BELOW`, `ELEVATED`, or an unresolved state |
| `compound` | compound label |
| `numeric_max`, `mrl_ngL` | recorded concentration summary and reporting limit, where available |
| `method_unit_era`, `Project`, `SampleName`, `source_row_ids` | provenance labels supplied by the caller |

Rows must already have passed unit, non-detect, replicate, and eligibility checks. `BELOW` means the result is *definitely* below the research threshold; it must not be assigned to an unresolved non-detect or missing result. Repeated assays for a date need to be resolved conservatively before calling the function. `gap` and `closure` are analysis choices, not biological constants.

The function returns an episode ledger, observation-state trace, and unanchored-high list. A first observed elevation is a sample observation; the actual onset may have happened earlier. The method does not infer concentrations between visits or describe customer exposure.

## Probability scoring

`metrics(y, p)` accepts binary observed outcomes and probabilities for the same evaluated records. Use an evaluation set that was not used to fit or tune the model. An empty set, a single outcome class, or too few events leaves some metrics undefined; the function returns `NaN` for those values.

`exact_interval(k, n)` calculates a binomial interval for a supplied count. Records collected on neighboring dates may not be independent, so do not treat that interval as an event-level or time-series uncertainty estimate without justifying the sampling unit.

This is an excerpt of the study code. It does not include source cleaning, time-of-availability logic, chronological splitting, model fitting, or the private input records needed to reproduce the full analysis.
