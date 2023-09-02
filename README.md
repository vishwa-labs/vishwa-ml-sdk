# MLMonitor - Automatic Instrumentation for ML Frameworks


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
default_labels = {"service": "ml-project-service", "k8s-cluster": "app0", "namespace": "dev"}

# Enable the auto-telemetry
LangchainTelemetry(default_labels=default_labels).auto_instrument()

```

## Documentation

- [Langchain](./docs/langchain.md) usage guide

## License

This project is licensed under the Apache License 2.0. See the LICENSE file for more details.


## Contributing

We welcome contributions to MLMonitor! If you're interested in contributing.

If you encounter any issues or have feature requests, please file an issue on our GitHub repository.
