## Logging Reference — VBOP Ingestion & Validation Pipeline

**Purpose:** what the pipeline records, where each record is written, and how long it is kept.
**Bucket:** `gs://vfie-dh-customer-complex-fixed` · **Project:** `vf-ie-dhk` · `europe-west1`

### Where logs are written

| # | What is logged | Destination | Written | Retention |
|---|---|---|---|---|
| 1 | **Application logs** — run progress, per-file outcome, warnings, errors, stack traces | **Cloud Logging** (stdout from the Cloud Run Function) | Continuously during a run | Cloud Logging default (30 days) |
| 2 | **Per-opportunity run log** — validation outcome and model cost | `vbop-ingestion-pipeline-logs/<DD-MM-YYYY>/<OPP-id>_<HHMMSS>.json` | One record per opportunity, per run | Indefinite (append-only history) |
| 3 | **Opportunity status report** — completeness across all opportunities | `_pipeline_state/opportunity_status.json` | Once per run | Overwritten each run (current state only) |
| 4 | **Validation result** — per-check verdicts and evidence | `…/processed_files/<OPP-id>/validation.json` | On each validation | Overwritten; history retained inside the file |
| 5 | **Processing ledger** — per-file state, not a log | `_pipeline_state/processed_files.json` | After every batch | Overwritten; deleting it forces full re-ingestion |
| 6 | **Infrastructure access** — who read/wrote GCS and BigQuery | **Cloud Audit Logs** | Automatic, platform-managed | Per Vodafone audit policy |

### 1. Application logs (Cloud Logging)

Standard Python logging to stdout, collected automatically. No custom sink. Includes: run id, files selected and skipped (with reason), each file parsed (`✓ <path>`), each failure with exception detail, LLM call outcomes and HTTP status, lock acquisition and release, and the run summary (`processed=N errors=N deferred=N`).

**Use for:** debugging a specific run, tracing why a file failed.

### 2. Per-opportunity run log — the primary operational record

One JSON object per opportunity, per run, under a date-partitioned prefix:

```json
{ "datetime": "14-09-2026 13:33:14", "run_id": "33d267f1",
  "opportunity_id": "OPP-0000000001",
  "validation_status": "N",
  "validations": { "VAL-001": "pass", "VAL-005": "fail", "VAL-014": "na" },
  "passed": 2, "failed": 1, "not_applicable": 1,
  "applicable_checks": 3, "score": "2/3",
  "documents_total": 4, "documents_parsed": 4, "failures": [],
  "input_tokens": 15000, "output_tokens": 1200,
  "total_tokens": 16200, "model_calls": 2 }
```

| Field group | Contents |
|---|---|
| Identity | `datetime` (DD-MM-YYYY HH:MM:SS), `run_id`, `opportunity_id` |
| Outcome | `validation_status`, per-check `validations` (pass / fail / na), `score` |
| Completeness | `documents_total`, `documents_parsed`, `failures` (file + reason) |
| Cost | `input_tokens`, `output_tokens`, `total_tokens`, `model_calls` |

**Every opportunity appears**, including those that could not be validated — those carry `validation_status: "not_validated"`, zero tokens, and the document failure that blocked them. `score` counts only *applicable* checks, so an order to which the circuit validations do not apply is not penalised for them.

**Use for:** cost tracking, trend analysis over time, per-opportunity audit trail.

### 3. Opportunity status report

Current-state view rewritten each run: totals (complete / failed), and for every failed opportunity the document count, parsed count, and each failure with its file and reason.

**Use for:** "what is broken right now, and why".

### 4. Validation result

Per opportunity: the headline verdict, human-readable reasoning, the full per-check report, resolution history (which checks were fixed since the last run and which requests can be closed), and reviewer `comments` — the one field the pipeline never overwrites.

### What is **not** logged

- **No application-level audit trail of user access.** Who viewed which opportunity in the review UI is not recorded by this pipeline; that is a separate planned component.
- **No document content in application logs.** Logs carry file paths and outcomes, not extracted values. Extracted content lives only in the parsed JSON under `processed_files/`.
- **No credentials or tokens** are logged at any level.

### Notes for review

- Items 2–5 sit in the same bucket as the data, under IAM control of that bucket.
- Item 2 grows without bound (one small object per opportunity per run). A lifecycle rule on `vbop-ingestion-pipeline-logs/` is recommended if retention beyond a defined period is not required.
- Item 1 inherits the project's Cloud Logging retention; extend via a log sink to GCS or BigQuery if a longer window is needed for audit.
