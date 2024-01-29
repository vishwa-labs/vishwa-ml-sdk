import os


api_key = os.environ.get("VISHWA_API_KEY")
host_url = os.environ.get("VISHWA_HOST_URL", "https://api.vishwa.ai")
adv_tracing_enabled = os.environ.get("VISHWA_TRACING_ENABLED", "false")
