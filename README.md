Hey team — quick recap of the solution we agreed on for (1) the waterfall chart visualization and (2) the KPI time-filtering issue, so we're aligned before testing.

**1. Waterfall chart visualization**
- We'll use ADK's built-in code executor tool.
- KPIs get written to a temp table in BigQuery.
- The agent writes a Python function to build the plot and runs it inside the sandboxed executor.
- Once the image is generated, we have two delivery options:
  - Stream the image bytes from backend to frontend directly, or
  - Write the image to a centralized GCS bucket and have the UI retrieve it from there.

**2. Time filtering — avoiding agent latency**
- Goal: avoid re-running the full agent (and eating that latency) every time a user changes the date range.
- KPI logic already exists as standalone Python functions, so we bypass the agent for the recompute step.
- When the user changes the date range (via chat or a UI button), the frontend calls the backend directly through an API to execute that function — no agent involved, which is significantly faster due to skipping agent delegation overhead.
- That function rewrites the KPIs in the table.
- Once the table is updated, the agent kicks back in to regenerate the plot for the new time range.

This is what we agreed on — we're moving into testing now and will report back with results.
