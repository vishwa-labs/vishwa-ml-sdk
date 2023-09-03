import uuid
from typing import Dict, Any

from langchain.chains.base import Chain

from xpuls.mlmonitor.langchain.decorators.telemetry_override_labels import TelemetryOverrideLabels
from xpuls.mlmonitor.langchain.handlers.callback_handlers import CallbackHandler

from xpuls.mlmonitor.langchain.profiling.prometheus import LangchainPrometheusMetrics


def patch_chain(ln_metrics: LangchainPrometheusMetrics):
    # Store the original run method
    original_run = Chain.run
    original_arun = Chain.arun

    def patched_run(self, *args, **kwargs):
        try:
            override_labels = TelemetryOverrideLabels._context.get()
            if override_labels is None:
                override_labels = {}
        except Exception as e:
            override_labels = {}
            print(f"Error getting labels. Exception: {e}")

        chain_run_id = str(uuid.uuid4())
        callback_handler = CallbackHandler(ln_metrics, chain_run_id, override_labels)
        with ln_metrics.agent_run_histogram.labels(**dict(ln_metrics.get_default_labels(), **override_labels)).time():
            if 'callbacks' in kwargs:
                kwargs['callbacks'].append(callback_handler)
            else:
                kwargs['callbacks'] = [callback_handler]

            # Call the original run method
            return original_run(self, *args, **kwargs)

    def patched_arun(self, *args, **kwargs):
        try:
            override_labels = TelemetryOverrideLabels._context.get()
            if override_labels is None:
                override_labels = {}
        except Exception as e:
            override_labels = {}
            print(f"Error getting labels. Exception: {e}")


        chain_run_id = str(uuid.uuid4())
        callback_handler = CallbackHandler(ln_metrics, chain_run_id, override_labels)
        with ln_metrics.agent_run_histogram.labels(**dict(ln_metrics.get_default_labels(), **override_labels)).time():
            if 'callbacks' in kwargs:
                kwargs['callbacks'].append(callback_handler)
            else:
                kwargs['callbacks'] = [callback_handler]

            # Call the original run method
            return original_arun(self, *args, **kwargs)

    # Patch the Chain class's run method with the new one
    Chain.run = patched_run
    Chain.arun = patched_arun
