import tiktoken

from chatgpt_long_term_memory.openai_engine.config import TokenCounterConfig


class TokenCounter:
    def __init__(self, token_counter_config: TokenCounterConfig, **kw):
        super().__init__(**kw)
        self.config = token_counter_config
        self.tt_encoding = tiktoken.get_encoding(self.config.encoding_model)

    def prompt_token_counter(self, prompt):
        tokens = self.tt_encoding.encode(prompt)
        total_tokens = len(tokens)
        return total_tokens
