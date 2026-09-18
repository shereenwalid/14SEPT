This turn: **`utils/bq_tokens.py`** only — the column names in the MERGE statement and the query parameter.

Across the whole token-reporting feature, four files:

- **`utils/bq_tokens.py`** — new file, the BigQuery MERGE writer
- **`utils/gemini_client.py`** — capture token usage from every parsing call (`TOKEN_USAGE`, `record_usage`, `get_usage`)
- **`pipeline.py`** — `_report_daily_tokens()`, called at the end of each run, combining parsing and validation usage
- **`utils/config_loader.py`** — new `TokensConfig` dataclass
- **`config.yaml`** — the `tokens:` section with the BSP dataset

Five, counting config. `utils/validation_step.py` already had the per-opportunity `METRICS` from earlier, so it didn't need changing — `pipeline.py` just reads it.
