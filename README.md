# 14SEPT

- 6 with bil

- Four changes. Starting with the validation catalogue:Now token accounting from the ADK events:Now the per-opportunity run log to GCS:All four done.

**VAL-024 (new) — VCES JIRA code.** `NA` when the provider type isn't VCES; `Y` when it is and a JIRA code is present anywhere (Tech Spec field, VCES sheet, order form, email body, attachment); `N` when it's VCES with no code. The agent states the code found and which document it came from.

**VAL-014 rewritten — Premise ID.** Now an *existence* check, not a format check, and it searches every document in the opportunity rather than just the Tech Spec — SIRO sheet, separate SIRO document, vendor quote, email body, attachment, or text recovered from an embedded image. The address alignment you described is included: where the Premise ID has an accompanying address, it's compared semantically against the Delivery Address from the Customer Information sheet, so abbreviations and punctuation differences don't count as mismatches, but a different building or Eircode does. If there's no accompanying address, it skips the comparison and says so rather than failing.

**VAL-018 removed.** The agent is explicitly told not to emit it, with the reason recorded (same value as the Delivery Address, already covered by VAL-002).

**Token logging.** Usage is captured from `usage_metadata` on each ADK event, using the approach you outlined. It accumulates across the whole agent turn — the test shows two model calls totalling 16,200 tokens for one opportunity, which is realistic since the tool-calling loop makes several calls per validation.

**Run logs** land at `gs://vfie-dh-customer-complex-fixed/vbop-ingestion-pipeline-logs/<DD-MM-YYYY>/<OPP-id>_<HHMMSS>.json` with everything you asked for: datetime, opportunity id, per-check pass/fail/na, `score` ("2/3"), parse failures, and input/output/total tokens.

One thing worth noting: `score` counts only *applicable* checks. An opportunity with 3 passes, 1 fail and 16 `NA` scores `3/4`, not `3/20` — otherwise every Kit order would look like it failed most of its checks when the circuit ones simply don't apply.

Opportunities that failed to parse still get a log record, with `validation_status: "not_validated"`, zero tokens and the specific file failure — so nothing is invisible.
