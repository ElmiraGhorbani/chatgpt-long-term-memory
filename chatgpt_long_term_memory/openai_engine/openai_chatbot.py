import openai

from chatgpt_long_term_memory.openai_engine.config import (ContextConfig,
                                                           OpenAIChatConfig,
                                                           TokenCounterConfig)
from chatgpt_long_term_memory.openai_engine.create_context import CreateContext
from chatgpt_long_term_memory.openai_engine.error_handler import \
    retry_on_openai_errors
from chatgpt_long_term_memory.openai_engine.token_counter import TokenCounter


class OpenAIChatBot:
    def __init__(self, openai_chatbot_config: OpenAIChatConfig, **kw):
        super().__init__(**kw)
        self.config = openai_chatbot_config
        self.prompt = self.config.prompt
        self.top_p = self.config.top_p
        self.presence_penalty = self.config.presence_penalty
        self.frequency_penalty = self.config.frequency_penalty 
        
        self.max_tokens = self.config.max_tokens
        self.token_counter = TokenCounter(
            token_counter_config=TokenCounterConfig())
        self.create_context = CreateContext(context_config=ContextConfig())

        self.models_max_tokens = {
            'gpt-4': 8192,
            'gpt-4-32k': 32768,
            'gpt-3.5-turbo': 4096,
            'gpt-3.5-turbo-16k': 16384
        }

    # @retry_on_openai_errors(max_retry=3)
    def chat(self, user_input, chat_history=[]):
        """
        This function is a wrapper for the OpenAI API and returns the chatbot response and the chat history with the user as a list of dictionaries
        :param user_input: the user's query
        :param chat_history: The chat history with the user as a list of dictionaries
        :return: The chatbot response and the chat history with the user as a list of dictionaries
        """
        if chat_history:
            history = "\n".join(chat_history)
        else:
            history = ""
        prompt = self.prompt.format(
            history, user_input)

        # check token to avoid max token limit error
        total_token = self.token_counter.prompt_token_counter(prompt)
        output_token = self.models_max_tokens[self.config.model_name] - (
            self.max_tokens + total_token)

        if output_token < 0 or output_token < self.max_tokens:
            summary_context = self.create_context.summarize_memories(
                history, self.token_counter.tt_encoding)
            prompt = self.prompt.format(
                summary_context, user_input)

        messages = [
            {"role": "system", "content": prompt},
        ]

        messages.append({"role": "user", "content": ""})

        response = openai.ChatCompletion.create(
            model=self.config.model_name,
            messages=messages,
            max_tokens=self.max_tokens,
            temperature=self.config.temperature,
            top_p=self.top_p,
            presence_penalty=self.presence_penalty,
            frequency_penalty=self.frequency_penalty,
        )
        messages.append(
            {"role": "assistant", "content": response["choices"][0]["message"].content})

        bot_response = response["choices"][0]["message"].to_dict()

        return bot_response["content"]
