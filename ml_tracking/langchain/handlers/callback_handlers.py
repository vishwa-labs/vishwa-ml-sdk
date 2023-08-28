import uuid
from datetime import datetime
import time
import logging
from typing import Any, Dict, List, Optional, Union
from langchain.callbacks.base import AsyncCallbackHandler

from langchain.schema.output import LLMResult
from langchain.schema.messages import BaseMessage

from langchain.schema.agent import AgentAction, AgentFinish

from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider

from ml_tracking.langchain.profiling.prometheus import LangchainChainMetrics, LangchainPrometheusMetrics, \
    LangchainChatModelMetrics, LangchainOpenAITokens
from ml_tracking.utils.common import get_safe_dict_value

# Set the tracer provider and a console exporter
trace.set_tracer_provider(TracerProvider())
trace.get_tracer_provider()

tracer = trace.get_tracer(__name__)


class CallbackHandler(AsyncCallbackHandler):
    log = logging.getLogger()

    def __init__(self, ln_metrics: LangchainPrometheusMetrics) -> None:
        logging.basicConfig()
        self.log.setLevel(logging.INFO)
        self.trace_id = str(uuid.uuid4())
        self.llm_start_time = None
        self.llm_end_time = None

        self.chat_start_time = None
        self.chat_end_time = None

        self.tool_start_time = None
        self.tool_end_time = None

        self.ln_metrics = ln_metrics

        self.chain_end_time = None
        self.chain_start_time = None
        self.chain_start_metrics = None

    def _get_model_name(self, data, model_type):
        if model_type == 'chat_models':
            model_info = get_safe_dict_value(get_safe_dict_value(
                get_safe_dict_value(data, 'kwargs', {}),
                'llm',
                {}
            ), 'kwargs', {})
            return model_info['model_name'] if 'model_name' in model_info else ''
        elif model_type == 'llm':
            return 'default'  ## TODO: Improve
        else:
            return 'default'

    def on_llm_start(
        self, serialized: Dict[str, Any], prompts: List[str], **kwargs: Any
    ) -> Any:
        """Run when LLM starts running."""

        self.log.info(f"on_llm_start, {serialized}, {prompts}, {kwargs}")

    def on_chat_model_start(
            self, serialized: Dict[str, Any], messages: List[List[BaseMessage]], **kwargs: Any
    ) -> Any:
        """Run when Chat Model starts running."""

        tags = get_safe_dict_value(kwargs, 'tags')
        parent_run_id = get_safe_dict_value(kwargs, 'parent_run_id')
        ml_model_name = get_safe_dict_value(get_safe_dict_value(serialized, 'kwargs', {}),
                                            'model_name', '')

        chat_model_start_metrics = LangchainChatModelMetrics(
            lc=str(get_safe_dict_value(serialized, 'lc')),
            type=get_safe_dict_value(serialized, 'type'),
            execution_step='on_chat_model_start',
            run_id=str(get_safe_dict_value(kwargs, 'run_id')),
            parent_run_id=str(parent_run_id) if parent_run_id is not None else None,
            agent_type=tags[0] if len(tags) > 0 else 'undefined',
            ml_model_type='chat_models',
            ml_model_name=ml_model_name,
            other_tags=','.join(list(tags)),
        )
        self.chat_start_time = time.time()  # Record start time
        self.ln_metrics.add_chat_model_counter(chat_model_start_metrics)

        self.log.debug(f"on_chat_model_start, {serialized}, {messages}, {kwargs}")

    def on_llm_new_token(self, token: str, **kwargs: Any) -> Any:
        """Run on new LLM token. Only available when streaming is enabled."""
        self.log.info(f"on_llm_new_token, {token}")

    def on_llm_end(self, response: LLMResult, **kwargs: Any) -> Any:
        """Run when LLM ends running."""
        tags = get_safe_dict_value(kwargs, 'tags')
        token_usage = get_safe_dict_value(response.llm_output, 'token_usage')
        if token_usage is not None:

            openai_tokens = LangchainOpenAITokens(
                execution_step='on_llm_end',
                run_id=str(get_safe_dict_value(kwargs, 'run_id')),
                parent_run_id=str(get_safe_dict_value(kwargs, 'parent_run_id')),
                ml_model_type='llm',
                ml_model_name=get_safe_dict_value(response.llm_output, 'model_name'),
                other_tags=','.join(list(tags)),
            )
            self.ln_metrics.add_openai_tokens_usage(openai_tokens,'prompt_tokens',
                                                    int(dict(token_usage)['prompt_tokens']))
            self.ln_metrics.add_openai_tokens_usage(openai_tokens, 'total_tokens',
                                                    int(dict(token_usage)['total_tokens']))
            self.ln_metrics.add_openai_tokens_usage(openai_tokens, 'completion_tokens',
                                                    int(dict(token_usage)['completion_tokens']))


        self.log.debug(f"on_llm_end, {response}, {kwargs}")

    def on_llm_error(
            self, error: Union[Exception, KeyboardInterrupt], **kwargs: Any
    ) -> Any:
        """Run when LLM errors."""
        self.log.debug("on_llm_error")

    def on_chain_start(self, serialized: Dict[str, Any], inputs: Dict[str, Any], **kwargs: Any) -> Any:
        """Run when chain starts running."""
        input_chars = get_safe_dict_value(inputs, 'input')
        chat_history_chars = get_safe_dict_value(inputs, 'chat_history')
        print(chat_history_chars)
        tags = get_safe_dict_value(kwargs, 'tags')
        parent_run_id = get_safe_dict_value(kwargs, 'parent_run_id')
        model_type = 'chat_models' if 'chat_models' in get_safe_dict_value(get_safe_dict_value(
            get_safe_dict_value(serialized, 'kwargs', {}),
            'llm',
            {}
        ), 'id', []) else 'llm'

        self.chain_start_metrics = LangchainChainMetrics(
            lc=str(get_safe_dict_value(serialized, 'lc')),
            type=get_safe_dict_value(serialized, 'type'),
            input_char_size=0 if input_chars is None or input_chars == '' else len(input_chars),
            chat_history_char_size=0 if chat_history_chars is None or chat_history_chars == '' else len(
                chat_history_chars),
            output_char_size=0,
            agent_type=tags[0] if len(tags) > 0 else 'Undefined',
            run_id=str(get_safe_dict_value(kwargs, 'run_id')),
            parent_run_id=str(parent_run_id) if parent_run_id is not None else None,
            ml_model_type=model_type,
            other_tags=','.join(list(tags)),
            ml_model_name=self._get_model_name(serialized, model_type),
            execution_step='on_chain_start',

        ).copy()

        self.chain_start_time = time.time()  # Record start time
        self.ln_metrics.add_chain_counter(self.chain_start_metrics)

        self.log.debug(f"on_chain_start, {serialized}, {inputs}, {kwargs}")

    def on_chain_end(self, outputs: Dict[str, Any], **kwargs: Any) -> Any:
        """Run when chain ends running."""
        output_chars = get_safe_dict_value(outputs, 'text')
        tags = get_safe_dict_value(kwargs, 'tags')
        parent_run_id = get_safe_dict_value(kwargs, 'parent_run_id')

        if self.chain_start_metrics is not None:
            chain_end_metrics = self.chain_start_metrics.model_copy(
                update={'run_id': str(get_safe_dict_value(kwargs, 'run_id')),
                        'output_char_size': 0 if output_chars is None or output_chars == '' else len(output_chars),
                        'parent_run_id': str(parent_run_id) if parent_run_id is not None else None,
                        'execution_step': 'on_chain_end'}, deep=True
            )
        else:
            chain_end_metrics = LangchainChainMetrics(
                lc='-1',
                type='undefined',
                input_char_size=0,
                chat_history_char_size=0,
                output_char_size=0 if output_chars is None or output_chars == '' else len(output_chars),
                agent_type=tags[0] if len(tags) > 0 else 'Undefined',
                run_id=str(get_safe_dict_value(kwargs, 'run_id')),
                parent_run_id=str(parent_run_id) if parent_run_id is not None else None,
                ml_model_type='llm',
                other_tags=','.join(list(tags)),
                ml_model_name='undefined',
                execution_step='on_chain_end',

            )

        elapsed_time = time.time() - self.chat_start_time

        self.ln_metrics.add_chain_counter(chain_end_metrics)
        self.ln_metrics.observe_chain_latency(chain_end_metrics, elapsed_time)
        self.log.debug(f"on_chain_end, {outputs}, {kwargs}, {self.chat_start_time}")

    def on_chain_error(self, error: Union[Exception, KeyboardInterrupt], **kwargs: Any) -> Any:
        """Run when chain errors."""
        tags = get_safe_dict_value(kwargs, 'tags')
        parent_run_id = get_safe_dict_value(kwargs, 'parent_run_id')

        if self.chain_start_metrics is not None:
            chain_err_metrics = self.chain_start_metrics.model_copy(
                update={'run_id': str(get_safe_dict_value(kwargs, 'run_id')),
                 'output_char_size': 0,
                 'parent_run_id': str(parent_run_id) if parent_run_id is not None else None,
                 'execution_step': 'on_chain_error'}, deep=True
            )
        else:
            chain_err_metrics = LangchainChainMetrics(
                lc='-1',
                type='undefined',
                input_char_size=0,
                chat_history_char_size=0,
                output_char_size=0,
                agent_type=tags[0] if len(tags) > 0 else 'Undefined',
                run_id=str(get_safe_dict_value(kwargs, 'run_id')),
                parent_run_id=str(parent_run_id) if parent_run_id is not None else None,
                ml_model_type='llm',
                other_tags=','.join(list(tags)),
                ml_model_name='undefined',
                execution_step='on_chain_error',

            )

        elapsed_time = time.time() - self.llm_start_time

        self.ln_metrics.add_chain_counter(chain_err_metrics)
        self.ln_metrics.observe_chain_latency(chain_err_metrics, elapsed_time)
        self.log.debug("on_chain_error")

    def on_tool_start(
            self, serialized: Dict[str, Any], input_str: str, **kwargs: Any
    ) -> Any:
        """Run when tool starts running."""
        self.log.info(f"on_tool_start, {serialized}, {input_str}, {kwargs}")

    def on_tool_end(self, output: str, **kwargs: Any) -> Any:
        """Run when tool ends running."""
        self.log.info(f"on_tool_end, {output}")

    def on_tool_error(
            self, error: Union[Exception, KeyboardInterrupt], **kwargs: Any
    ) -> Any:
        """Run when tool errors."""
        self.log.info("on_tool_error")

    def on_text(self, text: str, **kwargs: Any) -> Any:
        """Run on arbitrary text."""
        pass

    def on_agent_action(self, action: AgentAction, **kwargs: Any) -> Any:
        """Run on agent action."""
        self.log.debug(f"on_agent_action, {action}")

    def on_agent_finish(self, finish: AgentFinish, **kwargs: Any) -> Any:
        """Run on agent end."""
        self.log.debug(f"on_agent_finish, {finish}")
