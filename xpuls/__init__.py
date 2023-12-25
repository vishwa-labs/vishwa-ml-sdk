import os


api_key = os.environ.get("XPULSAI_API_KEY")
host_url = os.environ.get("XPULSAI_HOST_URL", "https://api.xpuls.ai")
adv_tracing_enabled = os.environ.get("XPULSAI_TRACING_ENABLED", "false")
