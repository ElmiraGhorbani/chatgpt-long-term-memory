import tiktoken

from chatgpt_long_term_memory.openai_engine.config import TokenCounterConfig


class TokenCounter:
    """
    This class represents a token counter that calculates the number of tokens in a given prompt.

    Attributes:
        config (TokenCounterConfig): An instance of the TokenCounterConfig class that holds the configuration
                                     parameters for the token counter.
        tt_encoding (tiktoken.Encoding): The token encoding model used to process the prompts and count tokens.

    Methods:
        __init__(self, token_counter_config: TokenCounterConfig, **kw): Constructor method for TokenCounter.
                                                                       Initializes the configuration and encoding model.
        prompt_token_counter(self, prompt: str) -> int: Calculates the number of tokens in the given prompt using
                                                       the specified encoding model.
                                                       Returns the total number of tokens as an integer.
    """

    def __init__(self, token_counter_config: TokenCounterConfig, **kw):
        # Initialize the base class (if applicable) and store the configuration.
        super().__init__(**kw)
        self.config = token_counter_config
        self.tt_encoding = tiktoken.get_encoding(self.config.encoding_model)

    def prompt_token_counter(self, prompt: str) -> int:
        """
        Calculate the number of tokens in the provided prompt using the encoding model.

        Parameters:
            prompt (str): The input prompt for which tokens need to be counted.

        Returns:
            int: The total number of tokens in the prompt.
        """
        tokens = self.tt_encoding.encode(prompt)
        total_tokens = len(tokens)
        return total_tokens
