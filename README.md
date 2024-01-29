# Welcome to vishwa.ai (formerly xpuls.ai) 👋 

## vishwa-ml-sdk
[![Twitter Follow](https://img.shields.io/twitter/follow/vishwa_ai?style=social)](https://x.com/vishwa_ai) [![Discord](https://img.shields.io/badge/Discord-Join-1147943825592045689?style=social)](https://social.vishwa.ai/join/discord)



<div align="center">
<a href="https://vishwa.ai">Website</a> | <a href="https://vishwa.ai/docs">Docs</a> | <a href="https://vishwa.ai/news">News</a> | <a href="https://x.com/vishwa_ai">Twitter</a> | <a href="https://social.vishwa.ai/join/discord">Discord</a>
</div>

[![PyPI version](https://badge.fury.io/py/vishwa-ml-sdk.svg)](https://badge.fury.io/py/vishwa-ml-sdk)
[![GitHub version](https://badge.fury.io/gh/vishwa-labs%2Fvishwa-ml-sdk.svg)](https://badge.fury.io/gh/vishwa-labs%2Fvishwa-ml-sdk)

## Roadmap 🚀

| Framework        | Status  |
|------------------|---------|
| Langchain        | ✅       |
| LLamaIndex       | Planned |
| PyTorch          | Planned |
| SKLearn          | Planned |
| Transformers     | Planned |
| Stable Diffusion | Next    |


### 💡 If support of any framework/feature is useful for you, please feel free to reach out to us via [Discord](https://social.vishwa.ai/join/discord) or Github Discussions


## 🔗 Installation 

1. Install from PyPI
```shell
pip install vishwa-ml-sdk
```

## 🧩 Usage Example 
```python
from vishwa.mlmonitor.langchain.instrument import LangchainTelemetry
import os
import vishwa
from vishwa.prompt_hub import PromptClient

# Enable this for advance tracking with our vishwa-ai platform
vishwa.host_url = "https://api.vishwa.ai"
vishwa.api_key = "********************"  # Get from https://platform.vishwa.ai
vishwa.adv_tracing_enabled = "true" # Enable this for automated insights and log tracing via xpulsAI platform
# Add default labels that will be added to all captured metrics
default_labels = {"service": "ml-project-service", "k8s_cluster": "app0", "namespace": "dev", "agent_name": "fallback_value"}

# Enable the auto-telemetry
LangchainTelemetry(default_labels=default_labels,).auto_instrument()
prompt_client = PromptClient(   
    prompt_id="clrfm4v70jnlb1kph240",  # Get prompt_id from the platform
    environment_name="dev"  # Deployed environment name
)

## [Optional] Override labels for scope of decorator [Useful if you have multiple scopes where you need to override the default label values]
@TelemetryOverrideLabels(agent_name="chat_agent_alpha")
@TagToProject(project_slug="defaultoPIt9USSR")  # Get Project Slug from platform
def get_response_using_agent_alpha(prompt, query):
    agent = initialize_agent(llm=chat_model,
                             verbose=True,
                             agent=CONVERSATIONAL_REACT_DESCRIPTION,
                             memory=memory)
    
    data = prompt_client.get_prompt({"variable-1": "I'm the first variable"})  # Substitute any variables in prompt

    res = agent.run(data) # Pass the entire `XPPrompt` object to run or invoke method
```

## ℹ️ Complete Usage Guides 

- [Langchain Framework](./docs/langchain.md) + [Grafana Template](./dashboards/grafana_langchain.json)

## 🧾 License 

This project is licensed under the Apache License 2.0. See the LICENSE file for more details.


## 📢 Contributing 

We welcome contributions to xpuls-ml-sdk! If you're interested in contributing.

If you encounter any issues or have feature requests, please file an issue on our GitHub repository.


## 💬 Get in touch 

👉 [Join our Discord community!](https://social.vishwa.ai/join/discord)

🐦 Follow the latest from vishwa.ai team on Twitter [@vishwa_ai](https://twitter.com/vishwa_ai)

📮 Write to us at [hello\@vishwa.ai](mailto:hello@vishwa.ai)
