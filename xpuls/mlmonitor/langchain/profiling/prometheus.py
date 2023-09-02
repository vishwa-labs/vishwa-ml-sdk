# Counters
from typing import Dict, Any, Optional, List

from prometheus_client import Counter, Histogram
from pydantic import BaseModel

chain_calls = Counter(
            'langchain_chain_calls',
            'Number of times method is called',
            ['type', 'lc', 'input_char_size', 'chat_history_char_size', 'run_id', 'parent_run_id',
             'agent_type', 'model_type', 'model_name', 'other_tags'])
chat_model_calls = Counter(
            'langchain_chain_chat_model_calls',
            'Counter for Langchain Chat Model Calls',
            ['type', 'lc', 'input_char_size', 'chat_history_char_size', 'run_id', 'parent_run_id',
             'agent_type', 'deployment_name', 'model_name', 'temperature'
             'other_tags'])
llm_model_calls = Counter(
            'langchain_chain_llm_model_calls',
            'Counter for Langchain Chat Model Calls',
            ['type', 'lc', 'input_char_size', 'chat_history_char_size', 'run_id', 'parent_run_id',
             'agent_type', 'deployment_name', 'model_name', 'temperature'
             'other_tags'])

#Histograms
llm_latency = Histogram(
            'langchain_chain_llm_latency',
            'LLM latency',
            ['trace_id']
        )
chain_latency = Histogram(
            'chain_latency',
            'Chain latency',
            ['trace_id']
        )

class LangchainChainMetrics(BaseModel):
    @classmethod
    def get_field_names(cls, alias=False):
        fields = list(cls.model_json_schema(alias).get("properties").keys())
        return fields

    lc: str
    type: str
    execution_step: str
    agent_type: str
    ml_model_type: Optional[str]
    ml_model_name: Optional[str]
    other_tags: Optional[str]
    # run_id: str
    # parent_run_id: Optional[str]
    # chain_run_id: str


class LangchainToolMetrics(BaseModel):
    @classmethod
    def get_field_names(cls, alias=False):
        fields = list(cls.model_json_schema(alias).get("properties").keys())
        return fields

    execution_step: str
    action: str
    agent_type: str
    other_tags: Optional[str]
    # run_id: str
    # parent_run_id: Optional[str]
    # chain_run_id: str


class LangchainOpenAITokens(BaseModel):
    @classmethod
    def get_field_names(cls, alias=False):
        fields = list(cls.model_json_schema(alias).get("properties").keys())
        return fields

    execution_step: str
    ml_model_type: Optional[str]
    ml_model_name: Optional[str]
    other_tags: Optional[str]
    # run_id: str
    # parent_run_id: Optional[str]
    # chain_run_id: str


class LangchainChatModelMetrics(BaseModel):
    @classmethod
    def get_field_names(cls, alias=False):
        fields = list(cls.model_json_schema(alias).get("properties").keys())
        return fields

    lc: str
    type: str
    execution_step: str
    agent_type: str
    ml_model_type: Optional[str]
    ml_model_name: Optional[str]
    other_tags: Optional[str]
    # chain_run_id: str
    # run_id: str
    # parent_run_id: Optional[str]


class LangchainPrometheusMetrics:
    def __init__(self, default_labels: Dict[str, Any]):
        chain_fields = LangchainChainMetrics.get_field_names() + list(default_labels.keys())
        chat_fields = LangchainChatModelMetrics.get_field_names() + list(default_labels.keys())
        openai_tokens_field = LangchainOpenAITokens.get_field_names() + list(default_labels.keys()) + ['usage_type']
        tools_field = LangchainToolMetrics.get_field_names() + list(default_labels.keys())
        self.default_labels = default_labels
        self.chain_execution_counter = Counter(
            'langchain_chain_execution',
            'Langchain Chain Lifecycle counter',
            chain_fields
        )
        self.chat_model_counter = Counter(
            'langchain_chat_model',
            'Langchain Chat Model counter',
            chat_fields
        )
        self.openai_tokens_counter = Counter(
            'langchain_openai_tokens',
            'Langchain OpenAI Tokens Count',
            openai_tokens_field
        )

        self.tools_usage_counter = Counter(
            'langchain_tools_usage',
            'Langchain tools Usage',
            tools_field
        )
        self.chain_execution_histogram = Histogram(
            'langchain_chain_latency',
            'Langchain chain Latency',
            chain_fields
        )

        self.chat_model_execution_histogram = Histogram(
            'langchain_chat_model_latency',
            'Langchain chat model Latency',
            chat_fields
        )

        self.tools_execution_histogram = Histogram(
            'langchain_tool_latency',
            'Langchain tool Latency',
            tools_field
        )

        ## Agent Run Latency
        self.agent_run_histogram = Histogram(
            'langchain_agent_run_latency',
            'Langchain Agent run end-to-end latency',
            list(default_labels.keys())
        )

    def get_default_labels(self):
        return self.default_labels

    def add_chain_counter(self, chain_metrics: LangchainChainMetrics):
        self.chain_execution_counter.labels(
            **dict(chain_metrics, **self.default_labels)
        ).inc()

    def add_tools_usage_counter(self, tool_metrics: LangchainToolMetrics):
        self.tools_usage_counter.labels(
            **dict(tool_metrics, **self.default_labels)
        ).inc()

    def add_openai_tokens_usage(self, openai_tokens: LangchainOpenAITokens,
                                usage_type: str, token_count: int):
        self.openai_tokens_counter.labels(
            **dict(openai_tokens, **self.default_labels, **{'usage_type': usage_type})
        ).inc(token_count)

    def add_chat_model_counter(self, chat_metrics: LangchainChatModelMetrics):
        self.chat_model_counter.labels(
            **dict(chat_metrics, **self.default_labels)
        ).inc()

    def observe_chain_latency(self, chain_metrics: LangchainChainMetrics, elapsed_time: float):

        self.chain_execution_histogram.labels(
            **dict(chain_metrics, **self.default_labels)
        ).observe(elapsed_time)

    def observe_tool_latency(self, tool_metrics: LangchainToolMetrics, elapsed_time: float):

        self.tools_execution_histogram.labels(
            **dict(tool_metrics, **self.default_labels)
        ).observe(elapsed_time)

    def observe_chat_model_latency(self, model_metrics: LangchainChatModelMetrics, elapsed_time: float):

        self.chat_model_execution_histogram.labels(
            **dict(model_metrics, **self.default_labels)
        ).observe(elapsed_time)

