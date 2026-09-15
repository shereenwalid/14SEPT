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




----------













1. Where the model gets called (line ~705)
async for _event in _runner.run_async(
    user_id="ui", session_id=session.id, new_message=msg
):
_runner is a Google ADK Runner (built from google.genai, imported at line 694). This line is what actually talks to Gemini's API over the network. The ADK sends your prompt, Gemini tokenizes it server-side, generates a response, tokenizes that too, and sends back a result — which the ADK wraps into a stream of _event objects that this async for loop iterates over.

Key point: no tokenization happens in this file. It all happens inside Gemini's infrastructure before the event ever reaches this loop.

2. Pulling the token counts off each event (lines 714-725)
# ---- cost metrics: accumulate model token usage per run ----
try:
    um = getattr(_event, "usage_metadata", None)
    if um is not None:
        _metrics_add_tokens(
            opp_id,
            getattr(um, "prompt_token_count", 0) or 0,
            getattr(um, "candidates_token_count", 0) or 0,
            getattr(um, "total_token_count", 0) or 0,
        )
except Exception:  # noqa: BLE001 - metrics never break a run
    pass
getattr(_event, "usage_metadata", None) — a plain attribute read. If this particular event carries usage data (it does for model-call events), um becomes that object; otherwise um is None and this block does nothing for that event.
getattr(um, "prompt_token_count", 0) etc. — again just reading fields off the object. These three numbers are exactly what Gemini's API reported for that one call: input tokens, output tokens, and total.
The try/except is defensive — if the event shape ever changes or usage_metadata is missing, metrics silently skip rather than crashing the whole agent run.
3. Accumulating across the run (lines 141-147)
def _metrics_add_tokens(opp_id: str, prompt: int, candidates: int, total: int):
    m = METRICS.get(opp_id)
    if not m:
        return
    m["input_tokens"] += int(prompt or 0)
    m["output_tokens"] += int(candidates or 0)
    m["total_tokens"] += int(total or (prompt or 0) + (candidates or 0))
An agent run can make several model calls (e.g. multiple ADK nodes/agents each calling Gemini). Every time step 2 fires, this function adds that call's tokens onto a running total for the whole opp_id run. So by the end, m["input_tokens"] is the sum of every prompt's token count Gemini reported, across every call in that run.

4. Using the totals to compute cost (lines 210-223)
big = m["input_tokens"] > BIG_PROMPT_TOKENS
rate_in  = RATE_IN_PER_1M_BIG  if big else RATE_IN_PER_1M
rate_out = RATE_OUT_PER_1M_BIG if big else RATE_OUT_PER_1M

cost_in   = m["input_tokens"]  / 1_000_000 * rate_in
cost_out  = m["output_tokens"] / 1_000_000 * rate_out
Here the accumulated, Gemini-reported totals get multiplied by the published per-million-token rates to produce a dollar figure. BIG_PROMPT_TOKENS (default 200,000) decides which Gemini 2.5 Pro pricing tier applies.

The whole path, visually
Gemini API (server-side tokenizer)
        │  returns usage_metadata in response
        ▼
ADK Runner wraps it into _event.usage_metadata
        │
        ▼
getattr(_event, "usage_metadata")     ← line 716, just reads it
        │
        ▼
_metrics_add_tokens(...)              ← line 141, sums it into METRICS[opp_id]
        │
        ▼
cost_in = input_tokens/1M * rate_in   ← line 215, turns tokens into $
At no point does this codebase run its own tokenizer or estimate token count from word/character count — it's entirely a pass-through of numbers Google's API already computed.
