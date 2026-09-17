Hi — thanks again for approving the Vision config PR. We've deployed and tried it, but image requests are still coming back 403:

"Image processing is disabled. Enable multimodal support by setting MULTIMODAL_SUPPORT=true in the environment variables."

Text-only calls to the same endpoint work fine, so it's specifically image content being refused. I couldn't find anything on Confluence about MULTIMODAL_SUPPORT, so I'm guessing it needs to be set on the proxy Cloud Run service itself rather than in the YAML?

Config we changed: [paste lab.yaml link]
Service: proxy-service-1034231601515.europe-west1.run.app (vf-ie-aib-prd-iei-cfa-lab, europe-west1)

Could you take a look, or point me to whoever owns the proxy deployment? Thanks!
