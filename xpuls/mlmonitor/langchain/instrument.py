from typing import Dict, Any
from langsmith import Client


from xpuls.mlmonitor.langchain.patches import patch_chain
from xpuls.mlmonitor.langchain.profiling.prometheus import LangchainPrometheusMetrics
from xpuls.mlmonitor.langchain.xpuls_client import XpulsAILangChainClient


class LangchainTelemetry:
    def __init__(self, default_labels: Dict[str, Any],
                 xpuls_host_url: str = "http://localhost:8000",
                 enable_prometheus: bool = True,
                 enable_otel_tracing: bool = True,
                 enable_otel_logging: bool = False):
        self.ln_metrics = LangchainPrometheusMetrics(default_labels)

        self.xpuls_client = XpulsAILangChainClient(
            api_url=xpuls_host_url
        )

        self.default_labels = default_labels
        self.enable_prometheus = enable_prometheus
        self.enable_otel_tracing = enable_otel_tracing
        self.enable_otel_logging = enable_otel_logging

    def auto_instrument(self):
        patch_chain(self.ln_metrics, self.xpuls_client)
        print("** ProfileML -> Langchain auto-instrumentation completed successfully **")
