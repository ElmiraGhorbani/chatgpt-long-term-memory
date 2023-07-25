import os

import openai

from chatgpt_long_term_memory.openai_engine.config import ContextConfig
from chatgpt_long_term_memory.openai_engine.error_handler import \
    retry_on_openai_errors

# Set the OpenAI API kEY using the environment variable or a default kEY
KEY = os.getenv("OPENAI_API_KEY",
                "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")
openai.api_key = KEY
os.environ["OPENAI_API_KEY"] = KEY


class CreateContext:
    def __init__(self, context_config: ContextConfig, **kw):
        super().__init__(**kw)
        self.config = context_config

        # like llama index summary prompt
        self.default_summary_prompt_tmpl = (
            "Write a summary of the following. Try to use only the "
            "information provided. "
            "Try to include as many key details as possible.\n"
            "\n"
            "\n"
            "{context_str}\n"
            "\n"
            "\n"
            'SUMMARY:"""\n'
        )

    def create_gpt_chunks(self, texts, tt_encoding):

        tokens = tt_encoding.encode(texts)
        total_tokens = len(tokens)

        chunks = []
        for i in range(0, total_tokens, self.config.chunk_size - self.config.chunk_overlap):
            chunk = tokens[i:i + self.config.chunk_size]
            chunks.append(tt_encoding.decode(chunk))
        return chunks

    @retry_on_openai_errors(max_retry=3)
    def summarize_memories(self, memories, tt_encoding):

        chuncks = self.create_gpt_chunks(
            memories, tt_encoding)
        final_responses = []
        for chunck in chuncks:
            prompt = self.default_summary_prompt_tmpl.format(
                context_str=chunck)
            messages = [
                {"role": "system", "content": prompt},
            ]
            user_massagge = {"role": "user", "content": ''}
            messages.append(user_massagge)
            response = openai.ChatCompletion.create(
                model=self.config.model_name,
                messages=messages,
                max_tokens=self.config.max_summary_token,
                temperature=self.config.summary_temperature,
                top_p=self.config.top_p,
                presence_penalty=self.config.presence_penalty,
                frequency_penalty=self.config.frequency_penalty,
            )
            text = response["choices"][0]["message"]["content"].strip()
            final_responses.append(text)
        text = ' '.join(final_responses)
        return text
