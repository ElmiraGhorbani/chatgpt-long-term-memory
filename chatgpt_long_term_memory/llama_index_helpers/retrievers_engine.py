import os

import openai
from llama_index.indices.query.schema import QueryBundle
from llama_index.retrievers import VectorIndexRetriever

from chatgpt_long_term_memory.llama_index_helpers.config import \
    RetrieversConfig
from chatgpt_long_term_memory.openai_engine.config import TokenCounterConfig
from chatgpt_long_term_memory.openai_engine.token_counter import TokenCounter

KEY = os.getenv("OPENAI_API_KEY",
                "")

openai.api_kEY = KEY
os.environ["OPENAI_API_KEY"] = KEY


class Retrievers:
    """
    Retrievers class handles querying the index with a given question to retrieve relevant responses.

    Args:
        top_k (int): Number of top results to retrieve.
        similarity_threshold (float): Similarity threshold for the retrieval results.

    """

    def __init__(self, retrieve_config: RetrieversConfig, **kw):
        super().__init__(**kw)
        self.config = retrieve_config
        self.top_k = self.config.top_k
        self.max_tokens = self.config.max_tokens

        self.token_counter = TokenCounter(
            token_counter_config=TokenCounterConfig())

        self.prompt_template = """Assistant is a large language model trained by OpenAI.

        Assistant is designed to be able to assist with a wide range of tasks, from answering simple questions to providing in-depth explanations and discussions on a wide range of topics. As a language model, Assistant is able to generate human-like text based on the input it receives, allowing it to engage in natural-sounding conversations and provide responses that are coherent and relevant to the topic at hand.

        Assistant is constantly learning and improving, and its capabilities are constantly evolving. It is able to process and understand large amounts of text, and can use this knowledge to provide accurate and informative responses to a wide range of questions. Additionally, Assistant is able to generate its own text based on the input it receives, allowing it to engage in discussions and provide explanations and descriptions on a wide range of topics.

        Overall, Assistant is a powerful tool that can help with a wide range of tasks and provide valuable insights and information on a wide range of topics. Whether you need help with a specific question or just want to have a conversation about a particular topic, Assistant is here to assist.

        History: {context}
        Human: {question}
        Assistant:"""

    def _answer_generator(self, question, retrieved_nodes):
        context = "\n".join(retrieved_nodes)
        prompt = self.prompt_template.format(
            context=context, question=question)
        messages = [
            {"role": "system", "content": prompt},
        ]
        total_token = self.token_counter.token_counter(prompt)
        check_token = 16384 - (
            self.max_tokens + total_token)

        assert check_token > 0, "Reached max tokens limit!"
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo-16k",
            messages=messages,
            max_tokens=self.max_tokens,
            temperature=0.7,
            top_p=1,
            presence_penalty=0,
            frequency_penalty=0,
        )

        messages.append(
            {"role": "assistant", "content": response["choices"][0]["message"].content})

        bot_response = response["choices"][0]["message"].to_dict()
        return bot_response['content']

    def query(self, index, question):
        """
        Query the index with a given question to retrieve relevant responses.

        Args:
            index: The index to query.
            question (str): The user's question or input.

        Returns:
            str: The response retrieved from the index based on the input question.
        """

        # Configure the vector retriever

        retrieved_nodes = self.get_nodes(question=question, index=index)
        response = self._answer_generator(question, retrieved_nodes)
        return response

    def get_nodes(self, question, index):

        # Configure the vector retriever
        retriever = VectorIndexRetriever(
            index=index,
            similarity_top_k=self.top_k,
        )
        # Perform the query and retrieve the response
        query_bundle = QueryBundle(question)
        nodes = retriever.retrieve(query_bundle)
        retrieved_nodes = [i.node.text for i in nodes]
        return retrieved_nodes
