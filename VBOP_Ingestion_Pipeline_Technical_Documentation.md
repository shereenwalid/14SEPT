# VBOP Quote-to-Order Ingestion & Validation Pipeline
## Technical Documentation

**Project:** VFIE Complex Fixed Products — Quote to Order
**Platform:** Google Cloud Platform, `vf-ie-dhk`, `europe-west1`
**Document status:** Technical reference
**Audience:** Solution architects, engineering leads, CTO office, client technical stakeholders

---

## 1. Executive summary

The pipeline converts the unstructured documents attached to Vodafone Ireland Complex Fixed opportunities — technical specifications, vendor quotes, customer purchase orders, order forms, email threads and their attachments — into structured JSON, then applies an automated quote-to-order validation checklist to each opportunity and publishes a machine-readable verdict.

It replaces a manual review step in which an operator opened each opportunity folder, read every document, and checked commercial and technical prerequisites by eye before an order could be raised.

**What it produces, per opportunity:**

| Artefact | Purpose |
|---|---|
| One JSON document per source file | Structured extraction of that document's content |
| `validation.json` | Pass/fail verdict against the VAL-Q2O checklist, with per-check evidence |
| `_versions.json` | Which source version produced each parsed file |
| `opportunity_status.json` (pipeline-level) | Which opportunities parsed completely, and why the others did not |

**Scale at time of writing:** approximately 1,756 opportunities and 29,419 source objects in the extract bucket, of which roughly 8,000–10,000 are current-version documents requiring extraction.

**Key design positions:**

- Extraction is **LLM-based**, not template-based. The document estate is heterogeneous and templates change without notice; a language model reads what is present rather than failing on an unexpected layout.
- Processing is **incremental and idempotent**. A document is parsed once and re-parsed only when its content changes.
- Validation is **all-or-nothing per opportunity**. A partially parsed opportunity produces no verdict, because a verdict derived from an incomplete document set is misleading in a way that a missing verdict is not.
- Retrieval for validation is **deterministic**, by opportunity identifier. There is no vector search or semantic retrieval in the current design (see §12).

---

## 2. Scope

### 2.1 In scope

- Ingestion of opportunity document folders from Google Cloud Storage
- Content extraction from 17 file extensions across 9 document families
- Recursive extraction of email attachments and ZIP archives
- Extraction of images embedded inside spreadsheets
- Per-opportunity document version resolution (original vs. `Modified-File` revisions)
- Automated validation against the VAL-Q2O checklist
- Validation resolution tracking across runs
- Operational tooling: audit, backfill, targeted re-processing

### 2.2 Out of scope

- Writing back to VBOP, BSP, SAP or MDG. The pipeline is read-only with respect to upstream systems.
- User interface. The pipeline publishes JSON to GCS; presentation is a separate component.
- Order placement. The pipeline determines readiness; it does not raise orders.
- Embedding generation and semantic search (see §12.2).

### 2.3 Relationship to the tabular ingestion pipeline

A sibling pipeline in this programme maps source files to BigQuery tables with a fixed column mapping. **This pipeline does not produce tables**, and the equivalent mapping contract here is *source file → parser → JSON document schema*, specified in §6. The reason is structural: the source documents do not share a stable field set. Two technical specifications for two opportunities may carry different sections, different sheet layouts and different field labels. A fixed relational schema would either discard content that does not fit or require a new column for every variant encountered. The JSON contract instead guarantees a stable *envelope* (`_meta`, `document_type`, `line_items`, and so on) while allowing the extracted field set to vary per document.

Where downstream consumers require tabular access, the recommended path is to load the published JSON into BigQuery as `JSON`-typed columns and project specific fields into views. This is a downstream concern and is not implemented by this pipeline.

---

## 3. Architecture

### 3.1 Component overview

```
┌──────────────────────────────────────────────────────────────────────┐
│  GCS: vfie-dh-customer-complex-fixed                                 │
│  └── VFIE-Complex-Fixed-Products-VBOP-Extracts/                      │
│      ├── <batch>_<OPP>_<time>/              ← original documents     │
│      ├── Modified-File/<batch>_<OPP>_<date>_<time>/  ← revisions     │
│      ├── Product Code/                      ← pass-through, unparsed │
│      └── parsed_files/                      ← pipeline output        │
└──────────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌──────────────────────────────────────────────────────────────────────┐
│  Ingestion Pipeline (Cloud Run Function, daily 08:00 Europe/Dublin)  │
│                                                                      │
│   1. Listing & version resolution                                    │
│   2. Change detection (ledger, object generation)                    │
│   3. Routing by extension → 9 parser families                        │
│   4. Text/table extraction (deterministic libraries)                 │
│   5. Structured extraction (Gemini 2.5 Flash via LLM proxy)          │
│   6. Output consolidation per opportunity                            │
│   7. Validation (ADK agent, per opportunity)                         │
│   8. State, audit and failure reporting                              │
└──────────────────────────────────────────────────────────────────────┘
           │                                    │
           ▼                                    ▼
┌────────────────────────┐        ┌──────────────────────────────────┐
│ LLM proxy (Cloud Run)  │        │ BigQuery — BSP reference data    │
│ → Vertex AI Gemini     │        │ (company & location lookups)     │
└────────────────────────┘        └──────────────────────────────────┘
```

### 3.2 Runtime

| Property | Value |
|---|---|
| Execution environment | Cloud Run Function (HTTP-triggered) |
| Schedule | Cloud Scheduler, `0 8 * * *`, Europe/Dublin |
| Per-invocation time budget | 450 s (below the 540 s platform timeout) |
| Parallelism — parsing | 12 workers |
| Parallelism — validation | 2 workers |
| Long-running mode | `backfill.py`, executed on a VM without the time budget |

The time budget is deliberately below the platform timeout so that state is always persisted before the platform terminates the process. Work not completed within the budget is reported as deferred and resumed on the next invocation.

### 3.3 External dependencies

| Dependency | Purpose | Failure behaviour |
|---|---|---|
| Google Cloud Storage | Source documents, output, state | Run fails; state preserved |
| LLM proxy → Vertex AI Gemini | Structured extraction, validation reasoning | Retries on transient errors; per-file failure otherwise |
| BigQuery (BSP datasets) | Company and location verification in validation | Check fails with reason; parsing unaffected |
| Google ADK | Validation agent runtime | Run aborts before validating (configurable) |

---

## 4. Source data model

### 4.1 Bucket layout

All input and output resides in `gs://vfie-dh-customer-complex-fixed` under the prefix `VFIE-Complex-Fixed-Products-VBOP-Extracts/`.

| Path pattern | Meaning |
|---|---|
| `<batch>_<OPP-id>_<HHMM>/` | Original document folder for an opportunity |
| `Modified-File/<batch>_<OPP-id>_<DDMMYYYY>_<HHMM>/` | A revised document set for the same opportunity |
| `Product Code/**` | Reference data. Synced but **never parsed**, by business rule |
| `parsed_files/<OPP-id>/` | Pipeline output, consolidated per opportunity |
| `_pipeline_state/` | Processing ledger, run lock, opportunity status report |

Opportunity folders arrive directly in this bucket. The previous cross-bucket synchronisation from `vfgrp-dh-advanced-analytics` is retained in configuration but disabled (`gcs.sync_enabled: false`).

### 4.2 Opportunity folder naming

Two forms are recognised:

| Form | Example | Interpretation |
|---|---|---|
| Dated | `8461_OPP-0007724692_05082026_1114` | Batch 8461, opportunity OPP-0007724692, revised 05-08-2026 at 11:14 |
| Undated | `8461_OPP-0007724692_1114` | Original submission; ranks older than any dated revision |

The 8-digit date component is interpreted as **DDMMYYYY** (`gcs.opp_date_format`). Folders that contain an OPP identifier but match neither pattern are accepted and treated as undated, with a log entry.

### 4.3 Document version resolution

Version resolution operates **per document**, not per folder. This is a material design decision.

A revised folder frequently re-sends only the documents that changed. If versioning operated at folder granularity, a document present in the original folder but absent from the revision would be treated as superseded and excluded — even though no newer version of it exists. In practice this silently removed technical specifications from the current document set.

The implemented rule:

> For each distinct document filename within an opportunity, the version carried by the most recent folder **containing that filename** is current. All earlier versions of that same filename are superseded.

| Scenario | Outcome |
|---|---|
| Same filename in original and revision | Revision is current; original superseded |
| Filename only in the original | Original remains current |
| Filename only in the revision | Revision is current |
| Filename changed between submissions | Treated as two distinct documents; both retained |

The final row is intentional. Establishing that `Tech Spec.xlsx` and `Tech Spec v2.xlsx` are the same document requires judgement the pipeline should not make unilaterally.

Superseded versions are **not parsed** and **not retained** in the output (`gcs.opp_archive_versions: false`). The opportunity folder holds exactly one parsed artefact per current document, overwritten in place when a newer version arrives. Source documents for all versions remain in the bucket and are unaffected.

---

## 5. Processing stages

### 5.1 Stage sequence

| # | Stage | Description |
|---|---|---|
| 1 | Lock acquisition | Atomic GCS object create (`if_generation_match=0`) prevents concurrent runs |
| 2 | Listing | Enumerate the input prefix; exclude pipeline output and Product Code paths |
| 3 | Version indexing | Resolve current vs. superseded per document (§4.3) |
| 4 | Change detection | Compare object generation against the ledger |
| 5 | Ordering | Sort pending work by opportunity so each completes before the next begins |
| 6 | Extraction | Route by extension; parse; publish JSON |
| 7 | Validation | Per opportunity, once all its documents are parsed |
| 8 | Reporting | Completeness assessment, opportunity status report, ledger persistence |
| 9 | Lock release | Released in all exit paths, including failure |

### 5.2 Change detection

A file is selected for processing when any of the following holds:

- It is absent from the ledger (never processed)
- Its GCS object **generation** differs from the recorded value (content changed)
- Its recorded status is `error` and its retry budget is not exhausted

A file is skipped when its status is `done` and its generation is unchanged, or when it is a superseded version, or when it resides under `Product Code/`.

Object generation is used rather than the last-modified timestamp because generation changes on every content overwrite and is not subject to clock or metadata anomalies.

### 5.3 Content de-duplication

Revised folders commonly re-send an entire document set with a single file changed. Where a pending file's MD5 (supplied by GCS at no cost) matches a file already parsed, the existing output is copied server-side rather than re-extracted. The hash index is held in the ledger and therefore persists across runs.

### 5.4 Ordering

Pending work is sorted by opportunity identifier so that all documents belonging to one opportunity are processed consecutively. Without this, an opportunity's documents are distributed across the entire run — its original folder and its `Modified-File` revisions sort far apart lexicographically — and the opportunity cannot be validated until near the end of the run.

---

## 6. Extraction contract — file type to output

This section is the analogue of a source-to-table column mapping.

### 6.1 Routing matrix

| Family | Extensions | Deterministic stage | LLM stage | Output suffix |
|---|---|---|---|---|
| `pdf` | `.pdf` | PyMuPDF text extraction | Text → JSON | `.pdf.json` |
| `docx` | `.docx`, `.doc` | python-docx paragraphs + tables | Text → JSON | `.docx.json` |
| `excel` | `.xlsx`, `.xls`, `.xlsm`, `.xlsb`, `.csv` | openpyxl / pandas (engine per format) | Cell map → layout JSON | `.xlsx_extracted.json` |
| `email` | `.msg`, `.eml` | extract-msg / stdlib `email` | Header+body → JSON | `.msg.json` |
| `image` | `.png`, `.jpg`, `.jpeg`, `.gif`, `.webp` | Magic-byte format detection | Image → JSON | `.png.json` |
| `text` | `.txt` | Direct read | Text → JSON | `.txt.json` |
| `pptx` | `.pptx` | python-pptx shapes, tables, notes | Text → JSON | `.pptx.json` |
| `visio` | `.vsdx`, `.vsdm` | OPC package XML shape text | Text → JSON | `.vsdx.json` |
| `archive` | `.zip` | Recursive extraction | Per contained file | Per contained file |

Files whose extension appears in no family are not parsed and are recorded as an opportunity failure (§9.2).

### 6.2 Output path construction

```
<input_prefix><parsed_prefix><OPP-id>/<original filename><suffix>
```

Worked example:

| Source object | Published output |
|---|---|
| `…/8461_OPP-0007724692_1114/Tech Spec.xlsx` | `…/parsed_files/OPP-0007724692/Tech Spec.xlsx_extracted.json` |
| `…/Modified-File/8462_OPP-0007724692_06082026_1426/Tech Spec.xlsx` | *same path* — overwrites the above |
| `…/8461_OPP-0007724692_1114/Quote.pdf` | `…/parsed_files/OPP-0007724692/Quote.pdf.json` |

The **full original filename including its extension** is retained in the output name. An earlier design stripped the extension, which caused `report.pdf`, `report.docx` and `report.msg` to resolve to a single output path and silently overwrite one another under parallel execution.

Email attachments and ZIP members are namespaced by their container:

| Source | Published output |
|---|---|
| Attachment `invoice.pdf` in `mail.msg` | `…/OPP-x/mail.msg_attachments/invoice.pdf.json` |
| `sub/inv.pdf` inside `batch.zip` | `…/OPP-x/batch.zip_extracted/sub/inv.pdf.json` |

### 6.3 Common output envelope

Every published document carries a `_meta` object. Fields common to all families:

| Field | Type | Description |
|---|---|---|
| `_meta.source_file` | string | Original filename as received |
| `_meta.parse_strategy` | string | Extraction route taken (family-specific values) |
| `error` | string | Present only on failure; human-readable cause |

Family-specific `_meta` fields:

| Family | Additional `_meta` fields |
|---|---|
| `pdf` | `total_pages`, `parse_strategy` (`text` \| `image`) |
| `docx` | `char_count` |
| `excel` | `form_block_count`, `table_block_count`, `confidence`, `hidden_sheets_skipped`, `sheet_visibility_known`, `embedded_image_count` |
| `email` | `attachment_count`, `attachment_names` |
| `image` | `size_bytes`, `mime_type`, `extraction_method`, `ocr_text_chars` |
| `pptx` | `slide_count`, `char_count` |
| `visio` | `page_count`, `char_count` |

### 6.4 Document JSON contract (non-spreadsheet families)

The extraction prompt specifies a stable top-level structure:

```json
{
  "document_type": "invoice | receipt | contract | report | form | email | other",
  "extracted_fields": { "<label>": "<value>" },
  "line_items": [ { } ],
  "dates": [ "<date>" ],
  "amounts": [ "<amount>" ],
  "parties": [ "<person or organisation>" ],
  "summary": "<one paragraph>",
  "confidence": "high | medium | low",
  "_meta": { }
}
```

| Key | Guarantee |
|---|---|
| `document_type` | Always present; constrained vocabulary |
| `extracted_fields` | Always present; **keys vary by document** — this is the deliberate flexibility point |
| `line_items` | Always present; empty array when the document has no tabular content |
| `dates`, `amounts`, `parties` | Always present; may be empty |
| `confidence` | Model's self-assessment; used for triage, not for pass/fail decisions |

### 6.5 Spreadsheet JSON contract

Spreadsheets use a distinct contract because their content is structural rather than prose. Sheets are classified into **form blocks** (label/value pairs) and **table blocks** (header row plus data rows):

```json
{
  "sheets": [
    {
      "sheet_name": "Customer Information",
      "blocks": [
        {
          "layout": "form",
          "title": "Customer Information",
          "fields": { "Customer Name": "Department of Social Protection" },
          "columns": [], "rows": [],
          "notes": null
        },
        {
          "layout": "table",
          "title": "Supplementary",
          "fields": {},
          "columns": ["Product Stock Code", "Quantity", "Cost Price", "Sell Price"],
          "rows": [ { "Product Stock Code": "R3J15A", "Quantity": "5" } ],
          "notes": null
        }
      ]
    }
  ],
  "confidence": "high",
  "_meta": { }
}
```

**Two extraction routes.** Workbooks below `excel.max_cells_for_gemini` (4,000 non-empty cells) are sent to the model as a cell map for layout inference. Larger workbooks bypass the model entirely and are loaded deterministically with pandas, producing table blocks only. `_meta.parse_strategy` records which route was taken.

**Data hygiene applied to spreadsheet output:**

| Rule | Rationale |
|---|---|
| Hidden and `veryHidden` sheets excluded | Working sheets are not part of the submitted document |
| Columns containing only nulls, placeholders or zeros dropped | Spreadsheet spacer columns carry no information |
| Placeholder strings (`nan`, `n/a`, `-`, `#REF!`, `#N/A`) treated as empty | Prevents placeholder text entering the record as data |
| Null-valued keys removed from each row | A row populates a subset of the sheet's columns |
| Embedded images extracted and parsed separately | Purchase orders are frequently pasted into a sheet as a screenshot |

Sheet visibility detection is format-specific: `sheet_state` via openpyxl for `.xlsx`/`.xlsm`; `visibility` via xlrd for `.xls`; direct parsing of `BrtBundleSh` records in `xl/workbook.bin` for `.xlsb`, which exposes no visibility API. Where visibility cannot be determined, **all sheets are processed** and `_meta.sheet_visibility_known` is set `false`, so detection failure never silently discards content.

### 6.6 Recursive containers

| Container | Behaviour | Limits |
|---|---|---|
| Email (`.msg`, `.eml`) | Each attachment routed to its own parser | Attachments named `*logo*` excluded |
| ZIP | Each member routed to its own parser | Nesting depth 2; 500 entries; 100 MB per entry; `__MACOSX` and dotfiles skipped |

A ZIP is treated as failed if any member fails, so its retry semantics apply to the archive as a whole. Re-processing is idempotent because successful members simply overwrite.

---

## 7. Validation layer

### 7.1 Design

Validation executes **once per opportunity**, after every document belonging to it has been parsed. It is implemented as a single tool-using agent (Google ADK) rather than a retrieval-augmented pattern.

Document retrieval is deterministic: the agent resolves an opportunity identifier to exactly one folder under `parsed_files/`, lists it, and loads the JSON documents it contains. Archived versions and pipeline metadata files are excluded. There is no ranking, chunking or similarity search — the unit of work is a known opportunity and the agent requires all of its documents, not the most relevant subset.

The agent holds five tools:

| Tool | Function |
|---|---|
| `get_opportunity_data` | Load all parsed documents for an opportunity from GCS |
| `lookup_bsp_company` | Verify customer and billing entity against BSP (BigQuery) |
| `lookup_bsp_location` | Verify service and delivery addresses against BSP (BigQuery) |
| `save_validation_status` | Persist the agent's own status record |
| `get_validation_status` | Read prior status, including human feedback |

The pattern is tool-using rather than retrieval-augmented because the BigQuery lookups are **data-dependent**: the model cannot know which company or address to verify until it has read the documents, so lookups must occur inside the reasoning loop.

### 7.2 Validation catalogue

Twenty checks are evaluated. Verdicts are `Y` (pass), `N` (fail) or `NA` (not applicable — used instead of `N` where a rule does not apply to the order type).

**Base validations — evaluated for every order**

| ID | Name | Rule | Action on failure |
|---|---|---|---|
| VAL-001 | Customer Name | Customer name in Tech Spec/Order Form exactly matches BSP | `raise_mdg` |
| VAL-002 | Delivery Address | Delivery address present in the Tech Spec | `raise_sales` |
| VAL-003 | Billing Entity | Billing entity matches the BSP invoicing customer name | `raise_mdg` |
| VAL-004 | Opportunity Reference | Opportunity reference exists in VBOP and matches exactly | `raise_sales` |
| VAL-005 | Customer PO | A customer PO, PO number or written confirmation exists | `raise_sales` |
| VAL-006 | Cost vs Sell Price | Vendor cost is below sell price on every line item | `raise_sales` |
| VAL-007 | Quantity | Quantities agree across Tech Spec, vendor quote, Vodafone quote and PO | `raise_sales` |
| VAL-008 | Vendor Quote Expiry | Vendor quote was valid **as at the customer quote date** | `raise_sales` |
| VAL-009 | Contact | Contact name and contact details present and complete | `raise_sales` |
| VAL-013 | Contract Term | A contract term is specified in the Tech Spec | `raise_sales` |
| VAL-023 | Recurring Item Contract Term | If any line item is recurring, a contract term must be set | `raise_sales` |

**Circuit validations — evaluated only for circuit orders; `NA` otherwise**

| ID | Name | Rule | Action on failure |
|---|---|---|---|
| VAL-014 | Premise ID | Present, populated and valid where the vendor is SIRO; `NA` otherwise | `raise_sales` |
| VAL-015 | Service | Service type present and consistent with supporting documents | `raise_sales` |
| VAL-016 | Speed | Circuit speed present and matching across order form and Tech Spec | `raise_sales` |
| VAL-017 | Product | Product name **or** product type present; fails only if both absent | `raise_sales` |
| VAL-018 | Service Address | Installation address present, and matching documents and BSP | `raise_mdg` |
| VAL-019 | Contact (Circuit) | Contact name and details in the circuit order form or Tech Spec | `raise_sales` |
| VAL-020 | PO (Circuit) | PO number present in the circuit order form and matching VBOP | `raise_sales` |
| VAL-021 | Billing Frequency | Billing frequency present and consistent with order requirements | `raise_sales` |
| VAL-022 | Recurring Order | PO type present and set to `Recurring` | `raise_sales` |

**VAL-008 reference-date semantics.** Vendor quote validity is assessed as at the **customer quote date**, not the processing date. An opportunity processed months after the fact must not fail because time has passed. The reference date is taken from the customer quote date, then the PO date, then the order form date, and only otherwise the processing date; the report states which was used. Where the quote was valid at the reference date but has since expired, the verdict remains `Y` and a staleness note is attached to the reasoning and to `needs_human_review`. The processing date is injected into each request, because the model cannot reliably determine the current date.

### 7.3 Validation output

Published to `parsed_files/<OPP-id>/validation.json`:

```json
{
  "validation": {
    "status": "N",
    "reasoning": "Blocking: Vendor quote expired. Failed checks — VAL-005: …",
    "comments": "",
    "date": "25-08-2026 14:22:57",
    "previous_status": "N",
    "resolved_checks": [],
    "open_requests": ["VAL-005"]
  },
  "opportunity_id": "OPP-0007724692",
  "resolution": {
    "resolved": [], "still_failing": ["VAL-005"],
    "new_failures": [], "regressed": []
  },
  "check_history": { "VAL-005": { } },
  "report": { "val_checks": [ ["VAL-001","Y","…","none"] ], "overall": { } }
}
```

| Field | Description |
|---|---|
| `validation.status` | `Y` or `N` — the headline verdict |
| `validation.reasoning` | Human-readable summary, including resolutions and advisory notes |
| `validation.comments` | **Written by the reviewing user.** Never overwritten by the pipeline |
| `validation.date` | Validation timestamp, `DD-MM-YYYY HH:MM:SS` |
| `validation.open_requests` | Checks whose failure raised an action that remains open |
| `resolution` | Change since the previous run (§7.4) |
| `check_history` | Per-check state, including `first_failed_at` |
| `report` | Full agent output, per-check, for detailed presentation |

All dates in this artefact use `DD-MM-YYYY`. The internal processing ledger retains ISO-8601, because change detection compares those values directly.

### 7.4 Resolution tracking

Each run compares its verdicts with the previous `validation.json`. A check that failed previously and now passes is recorded as **resolved**, rather than silently becoming a pass:

```json
{ "check": "VAL-005", "was": "N", "now": "Y",
  "first_failed_at": "20-08-2026 09:14:02",
  "resolved_at": "25-08-2026 14:22:57",
  "previously": "No PO document or customer confirmation found",
  "now_because": "PO 2403096 found in Modified-File customer PO email",
  "request_action": "raise_sales", "request_status": "resolved" }
```

Where the original failure raised an action (`raise_sales`, `raise_mdg`), that request is tagged `resolved` and removed from `open_requests`, allowing downstream workflow to close it. Regressions — a check that passed and now fails — are detected and flagged equivalently.

### 7.5 Re-validation triggers

An opportunity is re-validated when either:

1. Any of its documents was parsed during the run, or
2. Its **document fingerprint** changed since the last validation.

The fingerprint is a hash over each current document's path and object generation, held in the ledger. It changes on document addition, replacement or removal. This is the mechanism that closes a failed check when a missing purchase order subsequently arrives under `Modified-File` — including in cases where the new document required no parsing because its content was byte-identical to an existing file.

---

## 8. State management and concurrency

### 8.1 Processing ledger

`gs://vfie-dh-customer-complex-fixed/_pipeline_state/processed_files.json`

| Field | Purpose |
|---|---|
| `files[path].generation` | GCS object generation at time of processing |
| `files[path].status` | `done` \| `error` \| `failed` |
| `files[path].attempts` | Consecutive failure count |
| `files[path].last_error` | Diagnostic detail for the most recent failure |
| `content_hashes` | MD5 → output path, supporting de-duplication |
| `opp_fingerprints` | Opportunity → document-set hash, supporting re-validation |

The ledger is written after each batch and unconditionally at run end. Writes are throttled to respect the GCS limit of approximately one mutation per second per object, and rate-limit responses are retried with exponential backoff.

### 8.2 Concurrency control

A run lock is held at `_pipeline_state/run.lock`, created with `if_generation_match=0` so that acquisition is atomic. A second concurrent invocation — for example a manual run overlapping the schedule — receives HTTP 409 and exits without work. The lock is renewed once per minute during execution and released in all exit paths. A lock older than the 900-second lease is treated as abandoned and reclaimed, so a crashed run does not block the schedule indefinitely.

### 8.3 Failure handling

| Level | Behaviour |
|---|---|
| Transient LLM error (429, 5xx, timeout) | Retried with exponential backoff |
| Non-transient LLM error (400, safety block) | Not retried; recorded against the file |
| File failure | Retried on subsequent runs up to `max_file_attempts` (3) |
| Exhausted retries | Dead-lettered: skipped until the file's content changes |
| Validation agent unavailable | Run aborts before validating (`fail_fast`), with parsing state preserved |

---

## 9. Data quality and completeness

### 9.1 All-or-nothing per opportunity

An opportunity is validated only when **every** document in its current set has parsed successfully. This is a deliberate integrity constraint: a verdict derived from a partial document set carries the same authority as a complete one while being materially less reliable. A missing verdict prompts investigation; an incorrect one does not.

Any of the following marks an opportunity incomplete:

- A document failed to parse
- A document is dead-lettered
- A document's type has no parser
- A document has not yet been attempted

### 9.2 Opportunity status report

`gs://vfie-dh-customer-complex-fixed/_pipeline_state/opportunity_status.json`, rewritten each run:

```json
{
  "run_id": "6653e24b",
  "generated_at": "10-09-2026 13:51:22",
  "totals": { "opportunities": 1799, "complete": 5, "failed": 1794 },
  "failed_opportunities": {
    "OPP-0007081654": {
      "documents_total": 4,
      "documents_parsed": 3,
      "failures": [
        { "file": "…/po.pdf", "reason": "parse error: corrupt file", "attempts": 1 }
      ]
    }
  }
}
```

Every failed opportunity is listed with the specific file and the reason for each failure.

### 9.3 Audit tooling

| Tool | Purpose |
|---|---|
| `audit_opps.py` | Opportunity-level progress: total, complete, partial, not parsed, validated |
| `audit_missing.py` | File-level reconciliation of inputs against outputs and ledger, categorised by cause |
| `probe_proxy.py` | Determines which content types the LLM proxy currently accepts |

---

## 10. Operations

### 10.1 Invocation

| Mode | Command | Use |
|---|---|---|
| Scheduled | Cloud Scheduler → HTTP | Daily incremental run |
| Manual, full | `python backfill.py` | Backfill or bulk re-processing |
| Single opportunity | `python backfill.py --opp OPP-0007724692` | Targeted investigation |
| Validation only | `python backfill.py --validate-only` | Re-validate without re-extraction |
| Forced re-parse | `python backfill.py --opp <id> --force` | Ignore ledger state |
| Dry run | `GET /run?dry_run=true` | List pending work without processing |

`--opp` resolves an opportunity across its original folder and all `Modified-File` revisions, which a path-based filter cannot.

### 10.2 Configuration reference

| Key | Default | Purpose |
|---|---|---|
| `gcs.opp_grouping` | `true` | Consolidate output per opportunity |
| `gcs.opp_archive_versions` | `false` | Retain superseded versions |
| `gcs.parse_superseded_versions` | `false` | Parse non-current document versions |
| `gcs.sync_enabled` | `false` | Cross-bucket synchronisation |
| `gemini.model` | `gemini-2.5-flash` | Extraction model |
| `gemini.max_output_tokens` | `32768` | Output ceiling; lower values truncate large tables |
| `excel.max_cells_for_gemini` | `4000` | Threshold for deterministic spreadsheet handling |
| `runtime.max_workers` | `12` | Parallel extraction workers |
| `runtime.max_file_attempts` | `3` | Retries before dead-lettering |
| `validation.enabled` | `true` | Run the validation stage |
| `validation.fail_fast` | `true` | Abort if the agent cannot be loaded |
| `validation.revalidate_on_change` | `true` | Re-validate on document-set change |

### 10.3 Monitoring

Application logs are emitted to stdout and collected by **Cloud Logging**; no custom log sink is used. Infrastructure access is covered by **Cloud Audit Logs** on GCS and BigQuery. An application-level audit trail recording user access to the review interface is a separate, planned component and is not part of this pipeline.

Indicators warranting attention:

| Signal | Interpretation |
|---|---|
| Rising `failed` count in the opportunity status report | Systematic parsing issue |
| Repeated identical failure reasons | A missing parser or an upstream format change |
| `Validation agent unavailable` | Agent dependency or credential failure |
| HTTP 429 from the LLM proxy | Worker count above the proxy's sustainable rate |

---

## 11. Security and data governance

| Aspect | Position |
|---|---|
| Data residency | All storage and processing in `europe-west1` |
| Data movement | Documents are read from GCS and sent to Vertex AI Gemini via the internal LLM proxy. No third-party service is involved |
| Authentication | Service account identity; ID-token authentication to the proxy |
| Write scope | The pipeline writes only to its own output and state prefixes. Source documents are never modified or deleted |
| Upstream systems | Read-only. No writes to VBOP, BSP, SAP or MDG |
| Personal data | Documents contain business contact details. Content is processed transiently by the model; no data is retained by the model provider under the Vertex AI enterprise terms |
| Access control | Bucket-level IAM; the pipeline service account requires object read/write on the extract bucket only |

---

## 12. Known limitations

### 12.1 Image input currently blocked

The LLM proxy rejects image content, returning HTTP 403 with `Image processing is disabled. Enable multimodal support by setting MULTIMODAL_SUPPORT=true in the environment variables`. This affects scanned purchase orders, signed order forms, email image attachments and screenshots pasted into spreadsheets.

A request to enable multimodal support on the proxy is in progress. Until it is applied, a fallback chain operates: the image is wrapped in a single-page PDF and submitted as `application/pdf` (retaining native visual understanding if the proxy permits PDF parts); failing that, text is recovered locally by OCR and structured by the model. The extraction route is recorded in `_meta.extraction_method`, so OCR-derived values are distinguishable from natively extracted ones. OCR accuracy on numeric fields is materially lower than native vision, and values so derived should be treated as requiring confirmation.

### 12.2 No semantic retrieval

No embeddings are generated and no vector store is deployed. Retrieval is deterministic by opportunity identifier, which fits the current use case exactly. Should the requirement extend to open-ended enquiry across the opportunity estate, the assessed approach is `gemini-embedding-001` on Vertex AI with output truncated to 768 dimensions, and vectors held in either Vertex AI Vector Search or BigQuery. At current volumes, exhaustive similarity search in BigQuery would likely suffice without an approximate-nearest-neighbour index.

### 12.3 Legacy binary `.doc`

Word 97–2003 binary documents have no reliable pure-Python parser. Files misnamed `.doc` that are in fact `.docx` are detected by magic bytes and parsed normally. Genuine binary `.doc` files produce a diagnostic record and mark their opportunity incomplete. Resolution requires either an upstream conversion to `.docx` or a LibreOffice-based conversion step, the latter necessitating a container deployment.

### 12.4 Document identity by filename

Version resolution matches documents by filename. A document re-submitted under a different name is treated as a new document rather than a revision (§4.3).

### 12.5 State store scaling

The processing ledger is a single JSON object rewritten on each checkpoint. At present scale (approximately 3 MB) this is satisfactory. Growth is linear in processing history, and the mutation-rate limit on a single GCS object constrains checkpoint frequency. Migration to Firestore — one document per file, permitting per-record writes and direct querying — is the identified next step, scoped at approximately one engineering day.

---

## 13. Appendix A — Glossary

| Term | Definition |
|---|---|
| BSP | Vodafone billing and customer master data platform |
| MDG | Master Data Governance — the route for creating or amending customer records |
| VBOP | Vodafone Business Opportunity Platform — system of record for opportunities |
| OPP | Opportunity identifier, `OPP-<10 digits>` |
| SIRO | Fibre infrastructure vendor; triggers the Premise ID requirement (VAL-014) |
| Tech Spec | Technical specification workbook accompanying an opportunity |
| Modified-File | Bucket prefix holding revised document sets |
| Dead-letter | State of a file that has exhausted its retry budget |
| Fingerprint | Hash of an opportunity's document set, used to trigger re-validation |

## 14. Appendix B — Repository structure

| Path | Responsibility |
|---|---|
| `main.py` | Cloud Run Function entry point and HTTP routing |
| `pipeline.py` | Orchestration: listing, versioning, routing, completeness, reporting |
| `backfill.py` | Long-running execution without the platform time budget |
| `validation_agent.py` | ADK agent definition, tools and validation prompt |
| `config.yaml` | Runtime configuration |
| `parsers/` | One module per document family |
| `utils/gcs_helper.py` | Storage access, locking, state persistence |
| `utils/gemini_client.py` | LLM access, retry policy, content-type fallbacks |
| `utils/opp_versions.py` | Opportunity folder parsing and version ranking |
| `utils/validation_step.py` | Validation execution and resolution tracking |
| `utils/ocr.py` | OCR engines and PDF wrapping |
| `audit_opps.py`, `audit_missing.py`, `probe_proxy.py` | Operational tooling |
