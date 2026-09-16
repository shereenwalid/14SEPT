Hey team — quick recap of the solution we agreed on for (1) the waterfall chart visualization and (2) the KPI time-filtering issue, so we're aligned before testing.

**1. Waterfall chart visualization**
- We'll use ADK's built-in code executor tool.
- KPIs get written to a temp table in BigQuery.
- The agent writes a Python function to build the plot and runs it inside the sandboxed executor.
- Once the image is generated, we have two delivery options, with a tradeoff between them:
  - **Byte streaming (backend → frontend directly):** simpler, no extra storage step, but the image isn't persisted — each new plot overwrites/replaces the previous one in transit, so there's no history to go back to.
  - **GCS (centralized bucket):** adds a small write/retrieval step, but the image is persisted — we keep a durable copy, can retrieve past plots, and the UI just pulls from a stable location instead of depending on an active stream.
  - Leaning toward GCS for that persistence, but flagging both here since it affects how much plot history we can support later.

**2. Time filtering — avoiding agent latency**
- Goal: avoid re-running the full agent (and eating that latency) every time a user changes the date range.
- KPI logic already exists as standalone Python functions, so we bypass the agent for the recompute step.
- When the user changes the date range (via chat or a UI button), the frontend calls the backend directly through an API to execute that function — no agent involved, which is significantly faster due to skipping agent delegation overhead.
- That function rewrites the KPIs in the table.
- Once the table is updated, the agent kicks back in to regenerate the plot for the new time range.

This is what we agreed on — we're moving into testing now and will report back with results.
