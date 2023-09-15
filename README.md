# MLMonitor - Automatic Instrumentation for ML Frameworks

[![PyPI version](https://badge.fury.io/py/xpuls-mlmonitor.svg)](https://badge.fury.io/py/xpuls-mlmonitor)
[![GitHub version](https://badge.fury.io/gh/xpuls-labs%2Fxpuls-mlmonitor-python.svg)](https://badge.fury.io/gh/xpuls-labs%2Fxpuls-mlmonitor-python)
![Release built](https://github.com/xpuls-labs/xpuls-mlmonitor-python/actions/workflows/pypi-release/badge.svg?branch=main&x=1)

## Roadmap

- Prometheus Support for major ML & LLM frameworks
  - Langchain - Done
  - LLamaIndex - Coming Soon
  - SKLearn - Coming Soon
  - transformers - Coming Soon
  - pytorch - Coming Soon

## Installation

1. Install from PyPI
```shell
pip install xpuls-mlmonitor
```

## Usage Example
```python
from xpuls.mlmonitor.langchain.instrument import LangchainTelemetry

# Add default labels that will be added to all captured metrics
default_labels = {"service": "ml-project-service", "k8s_cluster": "app0", "namespace": "dev", "agent_name": "fallback_value"}

# Enable the auto-telemetry
LangchainTelemetry(default_labels=default_labels).auto_instrument()

## [Optional] Override labels for scope of decorator [Useful if you have multiple scopes where you need to override the default label values]
@TelemetryOverrideLabels(agent_name="chat_agent_alpha")
def get_response_using_agent_alpha(prompt, query):
    agent = initialize_agent(llm=chat_model,
                             verbose=True,
                             agent=CONVERSATIONAL_REACT_DESCRIPTION,
                             memory=memory)

    res = agent.run(f"{prompt}. \n Query: {query}")
```

## Complete Usage Guides

- [Langchain Framework](./docs/langchain.md) + [Grafana Template](./dashboards/grafana_langchain.json)

## License

This project is licensed under the Apache License 2.0. See the LICENSE file for more details.


## Contributing

We welcome contributions to MLMonitor! If you're interested in contributing.

If you encounter any issues or have feature requests, please file an issue on our GitHub repository.
