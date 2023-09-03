from typing import Dict, Any

from xpuls.mlmonitor.langchain.patches import patch_chain
from xpuls.mlmonitor.langchain.profiling.prometheus import LangchainPrometheusMetrics


class LangchainTelemetry:
    def __init__(self, default_labels: Dict[str, Any],
                 enable_prometheus=True,
                 enable_otel_tracing=True,
                 enable_otel_logging=False):
        self.ln_metrics = LangchainPrometheusMetrics(default_labels)

        self.default_labels = default_labels
        self.enable_prometheus = enable_prometheus
        self.enable_otel_tracing = enable_otel_tracing
        self.enable_otel_logging = enable_otel_logging

    def auto_instrument(self):
        patch_chain(self.ln_metrics)
        print("** ProfileML -> Langchain auto-instrumentation completed successfully **")

