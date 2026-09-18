This turn: **`utils/bq_tokens.py`** only — the column names in the MERGE statement and the query parameter.

Across the whole token-reporting feature, four files:

- **`utils/bq_tokens.py`** — new file, the BigQuery MERGE writer
- **`utils/gemini_client.py`** — capture token usage from every parsing call (`TOKEN_USAGE`, `record_usage`, `get_usage`)
- **`pipeline.py`** — `_report_daily_tokens()`, called at the end of each run, combining parsing and validation usage
- **`utils/config_loader.py`** — new `TokensConfig` dataclass
- **`config.yaml`** — the `tokens:` section with the BSP dataset

Five, counting config. `utils/validation_step.py` already had the per-opportunity `METRICS` from earlier, so it didn't need changing — `pipeline.py` just reads it.


---------------

Yes — you can test entirely with curl, no code change. And your mention of the frontend adding an `auth_token` header changes the picture, so let me cover both.

## Quick test: see what headers actually arrive

The simplest check is a temporary echo. But since you want **no code change**, use this instead — call your deployed backend with an identity token and see if it's accepted:

```bash
# get your own identity token
TOKEN=$(gcloud auth print-identity-token)

# call the deployed backend with it
curl -s -i -H "Authorization: Bearer $TOKEN" \
  https://<your-backend>.run.app/health
```

What the result tells you:
- **200 OK without the token too** → the service is `--allow-unauthenticated`. No identity reaches your app, which is exactly why `user` logs as `unknown`.
- **403/401 without the token, 200 with it** → authentication is enforced, and identity *is* arriving.

Test both ways:
```bash
curl -s -o /dev/null -w "no token: %{http_code}\n" https://<backend>.run.app/health
curl -s -o /dev/null -w "with token: %{http_code}\n" -H "Authorization: Bearer $TOKEN" https://<backend>.run.app/health
```

## Check the deployment setting directly

```bash
gcloud run services get-iam-policy <backend-service> --region europe-west1
```
If you see `allUsers` with `roles/run.invoker`, it's public → no identity, always `unknown`.

## The important bit: `auth_token` from the frontend

If your frontend is already sending an auth token in the header, that's a **different mechanism** from `X-Goog-Authenticated-User-Email`, and it may well contain the email you want — but my code doesn't read it.

A Google ID token is a JWT whose payload includes the user's email. You can decode one to see:

```bash
# paste the token the frontend sends
echo "<the-token>" | cut -d. -f2 | base64 -d 2>/dev/null | python3 -m json.tool
```

Look for an `email` claim. If it's there, **that's your source** — and the fix is to read and verify that token in `/log` and `/process` rather than relying on the IAP header.

So before changing anything, two things would settle it:

1. **What exactly does the frontend send?** The header name and an example token (redact the signature — the middle segment is enough to show the claims).
2. **Is the service public or auth-required?** (the curl test above)

If the frontend's token carries an `email` claim, I'd change the backend to extract it from there — that works whether or not IAP is enabled, and it's a small, contained change to the user-capture block. Tell me what the decode shows and I'll write it.
