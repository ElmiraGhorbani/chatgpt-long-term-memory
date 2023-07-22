import openai
import tiktoken

from chatgpt_long_term_memory.openai_engine.config import OpenAIChatConfig
from chatgpt_long_term_memory.openai_engine.error_handler import \
    retry_on_openai_errors


class OpenAIChatBot:
    def __init__(self, openai_chatbot_config: OpenAIChatConfig, **kw):
        super().__init__(**kw)
        self.config = openai_chatbot_config
        self.tt_encoding = tiktoken.get_encoding(self.config.encoding_model)
        self.chatbot_response = {
            "bot_response": "",
            "data": {
                "project_info": {
                }
            },
            "bot": {
                "bot_name": f"{self.model_name}",
                "bot_state": "chat_completion"
            },
        }
        self.models_max_tokens = {
            'gpt-4': 8192,
            'gpt-4-32k': 32768,
            'gpt-3.5-turbo': 4096,
            'gpt-3.5-turbo-16k': 16384
        }

    @retry_on_openai_errors(max_retry=3)
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
        # check token
        total_token = self.total_tokens(prompt)
        output_token = self.models_max_tokens[self.config.model_name] - (self.config.max_tokens + total_token)
        if output_token < 0 or output_token < self.config.max_tokens:
            #TODO
            # create summary
            pass
        messages = [
            {"role": "system", "content": prompt},
        ]

        messages.append({"role": "user", "content": ""})

        response = openai.ChatCompletion.create(
            model=self.config.model,
            messages=messages,
            max_tokens=self.config.max_tokens,
            temperature=self.config.temperature,
            top_p=self.config.top_p,
            presence_penalty=self.config.presence_penalty,
            frequency_penalty=self.config.frequency_penalty,
        )
        messages.append(
            {"role": "assistant", "content": response["choices"][0]["message"].content})

        bot_response = response["choices"][0]["message"].to_dict()

        # retun openai response and messages
        result = self.chatbot_response
        result["bot_response"] = bot_response["content"]
        result["memory"] = messages
        return result

    def token_counter(self, prompt):
        tokens = self.tt_encoding.encode(prompt)
        total_tokens = len(tokens)
        return total_tokens
