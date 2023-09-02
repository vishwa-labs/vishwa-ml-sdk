
## Langchain Documentation

### Basic Usage
```python
from xpuls.mlmonitor.langchain.instrument import LangchainTelemetry

# Add default labels that will be added to all captured metrics
default_labels = {"service": "ml-project-service", "k8s-cluster": "app0", "namespace": "dev"}

# Enable the auto-telemetry
LangchainTelemetry(default_labels=default_labels).auto_instrument()

```

### Advanced Guide
- #### Decorator for labelling agents in multi-agent systems [Optional] 
```python
@TelemetryExtraLabels(agent_name="default_agent", label2="value2")  # `TelemetryExtraLabels` Decorate the agent function
def get_default_agent_response(chat_model, memory, prompt_template, query): # Example function
    agent = initialize_agent(llm=chat_model,
                             verbose=True,
                             agent=CONVERSATIONAL_REACT_DESCRIPTION,
                             memory=memory)

    res = agent.run(f"{prompt_template}. \n Query: {query}")
```

