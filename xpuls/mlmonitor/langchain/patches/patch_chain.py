import uuid

from langchain.chains.base import Chain

from xpuls.mlmonitor.langchain.handlers.callback_handlers import CallbackHandler
from adapters.init_tracer import tracer

from xpuls.mlmonitor.langchain.profiling.prometheus import LangchainPrometheusMetrics


def patch_chain(ln_metrics: LangchainPrometheusMetrics):
    # Store the original run method
    original_run = Chain.run
    original_arun = Chain.arun

    def patched_run(self, *args, **kwargs):
        # print("Using patched run")
        chain_run_id = str(uuid.uuid4())
        callback_handler = CallbackHandler(ln_metrics, chain_run_id)
        with tracer.start_as_current_span("chain_run") as run_tracer:
            with ln_metrics.agent_run_histogram.labels(**dict(ln_metrics.get_default_labels())).time():
                if 'callbacks' in kwargs:
                    kwargs['callbacks'].append(callback_handler)
                else:
                    kwargs['callbacks'] = [callback_handler]

                # Call the original run method
                return original_run(self, *args, **kwargs)

    def patched_arun(self, *args, **kwargs):
        with tracer.start_as_current_span("chain_arun") as run_tracer:
            with ln_metrics.agent_run_histogram.labels(**dict(ln_metrics.get_default_labels())).time():
                if 'callbacks' in kwargs:
                    kwargs['callbacks'].append(CallbackHandler(ln_metrics))
                else:
                    kwargs['callbacks'] = [CallbackHandler(ln_metrics)]

                # Call the original run method
                return original_arun(self, *args, **kwargs)


    # Patch the Chain class's run method with the new one
    Chain.run = patched_run
    Chain.arun = patched_arun
