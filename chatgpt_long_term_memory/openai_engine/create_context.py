import os

import openai

from chatgpt_long_term_memory.openai_engine.config import ContextConfig
from chatgpt_long_term_memory.openai_engine.error_handler import \
    retry_on_openai_errors

# Set the OpenAI API kEY using the environment variable or a default kEY
KEY = os.getenv("OPENAI_API_KEY",
                "")
openai.api_key = KEY
os.environ["OPENAI_API_KEY"] = KEY


class CreateContext:
    """
    A class for managing context and summarizing memories using the OpenAI API.

    Attributes:
        default_summary_prompt_tmpl (str): A template to generate prompts for summarizing contexts.
                                          The template includes placeholders for context information.
        config (ContextConfig): An instance of ContextConfig containing configuration parameters
                                for the CreateContext class.

    Methods:
        __init__(self, context_config: ContextConfig, **kw):
            Initializes the CreateContext object with a given ContextConfig and any additional keyword arguments.

        create_gpt_chunks(self, texts, tt_encoding):
            Encodes a list of texts using the provided tokenizer (tt_encoding) and divides them into chunks
            based on the chunk_size and chunk_overlap specified in the ContextConfig.

            Args:
                texts (List[str]): List of texts to be encoded and divided into chunks.
                tt_encoding: Tokenizer used for encoding the texts.

            Returns:
                List[str]: List of text chunks.

        summarize_memories(self, memories, tt_encoding):
            Summarizes a list of memories using the GPT-3.5 Chat model from OpenAI.

            Args:
                memories (List[str]): List of memories to be summarized.
                tt_encoding: Tokenizer used for encoding the prompt.

            Returns:
                str: The summarized text.

    Note:
        This class requires an OpenAI API key to be set as an environment variable 'OPENAI_API_KEY'
        before using the OpenAI API for summarization. The key can be either provided directly or
        set in the environment using 'os.environ["OPENAI_API_KEY"]'.
    """

    def __init__(self, context_config: ContextConfig, **kw):
        """
        Initializes the CreateContext object with the given ContextConfig and any additional keyword arguments.

        Args:
            context_config (ContextConfig): An instance of ContextConfig containing configuration parameters
                                            for the CreateContext class.
            **kw: Additional keyword arguments that can be passed to the superclass.
        """
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
        """
        Encode a list of texts using the tokenizer (tt_encoding) and
        divide them into chunks based on the defined chunk_size and chunk_overlap.

        :param texts: List of texts to be encoded and divided into chunks.
        :param tt_encoding: Tokenizer used for encoding the texts.
        :return: List of text chunks.
        """

        tokens = tt_encoding.encode(texts)
        total_tokens = len(tokens)

        chunks = []
        for i in range(0, total_tokens, self.config.chunk_size - self.config.chunk_overlap):
            chunk = tokens[i:i + self.config.chunk_size]
            chunks.append(tt_encoding.decode(chunk))
        return chunks

    @retry_on_openai_errors(max_retry=3)
    def summarize_memories(self, memories, tt_encoding):
        """
        Summarize a list of memories using the GPT-3.5 Chat model from OpenAI.

        :param memories: List of memories to be summarized.
        :param tt_encoding: Tokenizer used for encoding the prompt.
        :return: The summarized text.
        """
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
