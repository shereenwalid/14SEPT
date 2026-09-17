## Logging Reference — Quote-to-Order Application

**Purpose:** what the application records, where each record is written, and how long it is kept.
**Bucket:** `gs://vfie-dh-customer-complex-fixed` · **Projects:** `vf-ie-aib-prd-iei-cfa-lab` (app) · `vf-ie-datahub` (data) · `europe-west1`

### Where logs are written

| # | What is logged | Destination | Written | Retention |
|---|---|---|---|---|
| 1 | **Application logs** — run progress, agent transitions, tool outcomes, warnings, errors | **Cloud Logging** (stdout from Cloud Run) | Continuously during a run | Cloud Logging default (30 days) |
| 2 | **Session activity log** — who used the app, for which opportunity, and what they raised | `VFIE-Complex-Fixed-Products-VBOP-Extracts/quote-to-order-app-logs/<date_time>_<session-id>.json` | On "Begin Order Creation"; updated when a request is raised | Indefinite (one object per session) |
| 3 | **Daily token usage** — model consumption per agent, per day | BigQuery `vfie_dh_lake_customer_complex_fixed_s.q2o_token_usage_daily` | After every run (accumulates into the day's row) | Indefinite (append/update history) |
| 4 | **Per-run cost report** — tokens, duration and BigQuery usage for one opportunity | `cost_reports/<OPP-id>_cost.txt` | End of every processing run | Ephemeral (container local disk) |
| 5 | **Validation feedback** — requests raised against failed checks | `…/parsed_files/<OPP-id>/validation.json` → `feedbacks[]` | When a user raises a request | Retained in the file, shared across users |
| 6 | **Infrastructure access** — who read/wrote GCS and BigQuery | **Cloud Audit Logs** | Automatic, platform-managed | Per Vodafone audit policy |

### 1. Application logs (Cloud Logging)

Standard Python logging to stdout, collected automatically. No custom sink. Tagged by area: `[process]` run start and outcome, `[exists]` opportunity folder check, `[app_log]` session log writes, `[validation]` validation file read and feedback saves, `[cost]` and `[tokens]` model and BigQuery usage, `[PCNAV]` and `[BQ ERROR]` product code lookups and query failures, `[prune]` document size reduction.

**Use for:** debugging a specific run, tracing why an opportunity failed.

### 2. Session activity log — the user audit record

One JSON object per user session, under the app-logs prefix:

```json
{ "session_id": "s-mfk2p9-a7c31d",
  "datetime": "2026-09-17T08:29:41Z",
  "user": "firstname.lastname@vodafone.com",
  "opp_id": "OPP-0007063044",
  "feedback": [
    { "id": "f-4b2e91c7", "check_key": "C24_vf_quote_to_customer_attached",
      "option": "raise_sales", "comment": "Chasing VF quote from sales",
      "by": "ui", "date": "2026-09-17T08:41:05Z" }
  ] }
```

| Field group | Contents |
|---|---|
| Identity | `session_id`, `datetime` (ISO 8601 UTC), `user` |
| Subject | `opp_id` — the opportunity searched |
| Actions | `feedback[]` — each request raised: `id`, `check_key`, `option`, `comment`, `by`, `date` |

**One file per session, not per opportunity**, so two users working the same opportunity are recorded separately. `feedback[]` contains **only the requests raised in that session** — requests raised previously by other users are not copied in. `user` is taken from the Cloud Run authenticated-user header; where authentication is not enforced it records `unknown`.

**Use for:** user activity audit, "who raised what, and when".

### 3. Daily token usage (BigQuery)

One row per agent per day, updated in place so the day's totals accumulate as runs complete.

| Column | Type | Contents |
|---|---|---|
| `agent_name` | STRING | `qto_retrieval_agent`, `product_code_agent`, `bsp_extraction_agent`, `email_agent` |
| `usage_date` | DATE | Partition key |
| `input_tokens` | INT64 | Prompt tokens consumed that day |
| `output_tokens` | INT64 | Completion tokens produced that day |
| `total_tokens` | INT64 | Sum of the two |

Written via `MERGE`, so a run adds to the existing row rather than creating duplicates. Table is date-partitioned on `usage_date`.

**Use for:** model cost tracking and trend analysis by agent over time.

### 4. Per-run cost report

Human-readable record of one opportunity's cost drivers and the calculation applied:

```
MEASURED PER RUN
  duration                : 75.07 s
  input tokens            : 145,372
  output tokens           : 1,542
  BigQuery queries        : 4
  BigQuery bytes scanned  : 40.00 MB
  sales order rows written: 2

COST PER SERVICE  (rates and equation shown per line)
```

**Use for:** per-opportunity cost evidence during testing.

### 5. Validation feedback

Requests raised against failed checks are appended to `feedbacks[]` inside the opportunity's `validation.json`. This is the shared record — visible to every user who opens that opportunity — and is what gates progression to order creation. The agent's own check results are never overwritten by user feedback.

### What is **not** logged

- **No document content.** Logs carry opportunity ids, check keys and outcomes, not extracted values. Extracted content lives only in the order output and the parsed files.
- **No credentials or tokens** are logged at any level.
- **No page-level user tracking.** Which screens a user viewed is not recorded — only the opportunity searched and the requests raised.

### Notes for review

- Items 2 and 5 sit in the same bucket as the data, under IAM control of that bucket.
- Item 2 grows without bound (one small object per session). A lifecycle rule on `quote-to-order-app-logs/` is recommended if retention beyond a defined period is not required.
- **Item 4 is ephemeral.** Cost reports are written to container local disk and are lost when the Cloud Run instance recycles. If they are needed as a durable record they should be written to GCS alongside item 2.
- Item 1 inherits the project's Cloud Logging retention; extend via a log sink to GCS or BigQuery if a longer window is needed for audit.
