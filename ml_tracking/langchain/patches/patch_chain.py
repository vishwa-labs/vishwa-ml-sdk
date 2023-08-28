from langchain.chains.base import Chain

from ml_tracking.langchain.handlers.callback_handlers import CallbackHandler
from adapters.init_tracer import tracer
from prometheus_client import Histogram

from ml_tracking.langchain.profiling.prometheus import LangchainPrometheusMetrics

# Store the original run method
original_run = Chain.run
original_arun = Chain.arun

h = Histogram('chain_run_latency_seconds', 'Description of histogram for Chain Run Latency Seconds',
              labelnames=("service", "env", "model"))
har = Histogram('chain_arun_latency_seconds', 'Description of histogram for Chain Arun Latency Seconds',
                labelnames={"service": 'jm-money-agent-ai', "env": 'dev', "model": "gpt-3.5"})

ln_metrics = LangchainPrometheusMetrics({"service": 'jm-money-agent-ai', "env": 'dev', "model": "gpt-3.5"})

def patched_run(self, *args, **kwargs):
    print("Using patched run")
    callback_handler = CallbackHandler(ln_metrics)
    with tracer.start_as_current_span("chain_run") as run_tracer:
        # h.labels()
        with h.labels(service="jm-money-agent-ai", env="dev",model="gpt-3.5").time():
        # with h.time():
            if 'callbacks' in kwargs:
                kwargs['callbacks'].append(callback_handler)
            else:
                kwargs['callbacks'] = [callback_handler]

            # Call the original run method
            return original_run(self, *args, **kwargs)


def patched_arun(self, *args, **kwargs):
    with tracer.start_as_current_span("chain_arun") as run_tracer:
        with har.time():
            if 'callbacks' in kwargs:
                kwargs['callbacks'].append(CallbackHandler(ln_metrics))
            else:
                kwargs['callbacks'] = [CallbackHandler(ln_metrics)]

            # Call the original run method
            return original_arun(self, *args, **kwargs)


# Patch the Chain class's run method with the new one
Chain.run = patched_run
Chain.arun = patched_arun
