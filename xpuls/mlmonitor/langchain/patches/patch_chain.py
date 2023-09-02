import uuid
from typing import Dict, Any

from langchain.chains.base import Chain

from xpuls.mlmonitor.langchain.decorators.telemetry_extra_labels import TelemetryExtraLabels
from xpuls.mlmonitor.langchain.handlers.callback_handlers import CallbackHandler

from xpuls.mlmonitor.langchain.profiling.prometheus import LangchainPrometheusMetrics


def patch_chain(default_labels: Dict[str, Any]):
    # Store the original run method
    original_run = Chain.run
    original_arun = Chain.arun

    def patched_run(self, *args, **kwargs):
        try:
            extra_labels = TelemetryExtraLabels._context.get()
            if extra_labels is None:
                extra_labels = {}
        except Exception as e:
            extra_labels = {}
            print(f"Error getting labels. Exception: {e}")

        chain_run_id = str(uuid.uuid4())
        agg_labels = dict(default_labels, **extra_labels)
        ln_metrics = LangchainPrometheusMetrics(agg_labels)
        callback_handler = CallbackHandler(ln_metrics, chain_run_id)
        with ln_metrics.agent_run_histogram.labels(**ln_metrics.get_default_labels()).time():
            if 'callbacks' in kwargs:
                kwargs['callbacks'].append(callback_handler)
            else:
                kwargs['callbacks'] = [callback_handler]

            # Call the original run method
            return original_run(self, *args, **kwargs)

    def patched_arun(self, *args, **kwargs):
        try:
            extra_labels = TelemetryExtraLabels._context.get()
            if extra_labels is None:
                extra_labels = {}
        except Exception as e:
            extra_labels = {}
            print(f"Error getting labels. Exception: {e}")
        chain_run_id = str(uuid.uuid4())
        agg_labels = dict(default_labels, **extra_labels)
        ln_metrics = LangchainPrometheusMetrics(agg_labels)
        callback_handler = CallbackHandler(ln_metrics, chain_run_id)
        with ln_metrics.agent_run_histogram.labels(**ln_metrics.get_default_labels()).time():
            if 'callbacks' in kwargs:
                kwargs['callbacks'].append(callback_handler)
            else:
                kwargs['callbacks'] = [callback_handler]

            # Call the original run method
            return original_arun(self, *args, **kwargs)

    # Patch the Chain class's run method with the new one
    Chain.run = patched_run
    Chain.arun = patched_arun
