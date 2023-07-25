import openai

from chatgpt_long_term_memory.openai_engine.config import (ContextConfig,
                                                           OpenAIChatConfig,
                                                           TokenCounterConfig)
from chatgpt_long_term_memory.openai_engine.create_context import CreateContext
from chatgpt_long_term_memory.openai_engine.error_handler import \
    retry_on_openai_errors
from chatgpt_long_term_memory.openai_engine.token_counter import TokenCounter


class OpenAIChatBot:
    """
    This class represents a chatbot powered by OpenAI's language model and provides an interface to interact with the model
    to generate responses to user queries.

    Attributes:
        config: An instance of OpenAIChatConfig class containing the configuration settings for the chatbot.
        prompt: The initial prompt/template used for generating chatbot responses.
        top_p: The nucleus sampling parameter (top-p) used during response generation.
        presence_penalty: The presence penalty parameter used during response generation.
        frequency_penalty: The frequency penalty parameter used during response generation.
        max_tokens: The maximum number of tokens allowed for the chatbot's response.

        token_counter: An instance of TokenCounter used to count tokens in chat history and responses.
        create_context: An instance of CreateContext used to summarize chat history and manage context.

        models_max_tokens: A dictionary containing the maximum number of tokens allowed for different models.

    Methods:
        chat(user_input, chat_history=[]):
            This function is a wrapper for the OpenAI API and returns the chatbot response and the chat history with the user as a list of dictionaries.
            It takes user_input (the user's query) and chat_history (the chat history with the user) as input and returns the chatbot response as a string.
    """

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

    @retry_on_openai_errors(max_retry=3)
    def chat(self, user_input, chat_history=[]):
        """
        This function serves as a wrapper for the OpenAI API, allowing the chatbot to generate a response to a user's query.
        The chatbot uses the specified language model and the provided chat history to generate context-aware responses.

        :param user_input: The user's query, a string containing the input text for the chatbot.
        :param chat_history: (Optional) The chat history with the user as a list of dictionaries, where each dictionary contains the 'role' (e.g., "user", "assistant") and 'content' (the content of the message). Defaults to an empty list.
        :return: A string representing the chatbot's response to the user's input.

        The chatbot follows these steps during the response generation:
        1. The chat history is combined into a single string to create a context for the chatbot's response.
        2. The 'prompt' attribute in the chatbot's configuration is used to format the user's query within the context.
        3. The total number of tokens in the formatted prompt is counted using the 'token_counter' instance.
        4. The available token limit for the language model is calculated, considering the model's maximum token limit and the maximum token limit set for the chatbot.
        5. If the available token limit is insufficient to accommodate the response, the chatbot summarizes the chat history using the 'create_context' instance and updates the prompt accordingly.
        6. The chatbot sends a request to the OpenAI API using the 'openai.ChatCompletion.create()' method, passing the formatted prompt and other configuration settings.
        7. The API returns a response that contains the generated message from the language model.
        8. The chatbot extracts the assistant's response from the API response and returns it as the final output.
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
