Hi — could you help us enable image input on the AI Booster proxy for our instance?

**Instance:** vf-ie-aib-prd-iei-cfa (lab)
**Service:** proxy-service-1034231601515.europe-west1.run.app
**Project:** vf-ie-aib-prd-iei-cfa-lab, europe-west1
**Model:** gemini-2.5-pro (also gemini-2.5-flash, which we may switch back to)

**What we're seeing**

Any request containing an image part is rejected by the proxy:

    POST .../models/gemini-2.5-pro:generateContent  ->  HTTP 403 Forbidden
    {"error": {"message": "Image processing is disabled. Enable multimodal support
     by setting MULTIMODAL_SUPPORT=true in the environment variables."}}

Text-only requests to the same endpoint return 200 OK, so this is not auth, quota or connectivity — it is specifically image content being refused.

**What we've already done**

We added a Vision block under the gemini-2.5-pro entry in instances/vf-ie-aib-prd-iei-cfa/lab.yaml (input_checks.Vision, with thresholds for Toxic, Sexual, Violent, Health, Finance and the rest), so image moderation policy is now defined. We are still getting the same 403, which we read as the config defining how images are moderated once accepted, while MULTIMODAL_SUPPORT controls whether an image part is accepted at all.

**What we think is needed — could you confirm?**

1. MULTIMODAL_SUPPORT=true set as an environment variable on the proxy Cloud Run service, with a new revision deployed.
2. Confirmation of whether our lab.yaml Vision change needs a redeploy of the proxy to take effect, or is picked up automatically.

If the env var is not the right mechanism for this deployment, please let us know what is — we are going on the wording of the error message.

**Why it matters for us**

We ingest Vodafone Ireland Complex Fixed opportunity documents. A material share of the evidence we need is only available as images: scanned and photographed customer purchase orders, signed order forms, and screenshots of PO approval emails pasted into technical specification spreadsheets. Without image input we cannot read those, and validations such as "is the customer PO present" and "is the PO/quote signed" cannot be answered reliably.

We have an OCR fallback in place so the pipeline is not blocked, but OCR is materially less accurate on the fields that matter most — PO numbers and contract terms are exactly where digit misreads occur — so we would much rather use native image understanding.

**One quick question on scope:** are PDF parts (application/pdf) currently permitted on this instance? If PDFs containing images are accepted, that would give us a usable route in the meantime.

Happy to jump on a call or share a reproducible request if that is easier.

Thanks.
