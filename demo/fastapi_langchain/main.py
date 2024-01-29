import os

from fastapi import FastAPI
from starlette.middleware.gzip import GZipMiddleware
from starlette_exporter import PrometheusMiddleware, handle_metrics

from vishwa.mlmonitor.langchain.instrument import LangchainTelemetry

service_name = "Vishwa AI demo service"
app = FastAPI(
    title=service_name,
    description="",
    version="0.0.1"
)
app.add_middleware(GZipMiddleware, minimum_size=1000)
app.add_middleware(PrometheusMiddleware, app_name=service_name, group_paths=True)
app.add_route("/metrics", handle_metrics)  # Metrics are published at this endpoint

# Initialise vishwa.ai
default_labels = {"service": "vishwai-demo-service", "namespace": "mlops",
                  "agent_name": "not_found"}

os.environ["VISHWA_TRACING_ENABLED"] = "true"  # ENABLE THIS ONLY IF ADVANCED vishwa.ai MONITORING IS REQUIRED

# xpuls_host_url is an optional parameter and required if `VISHWA_TRACING_ENABLED` is enabled
LangchainTelemetry(default_labels=default_labels, xpuls_host_url='https://api.vishwa.ai').auto_instrument()

@app.get('/healthcheck')
def health_check():
    return "ping!"
