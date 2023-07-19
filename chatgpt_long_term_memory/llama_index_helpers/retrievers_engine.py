import os

import openai
from llama_index.indices.postprocessor import SimilarityPostprocessor
from llama_index.query_engine import RetrieverQueryEngine
from llama_index.retrievers import VectorIndexRetriever

from chatgpt_long_term_memory.llama_index_helpers.config import \
    RetrieversConfig

KEY = os.getenv("OPENAI_API_KEY",
                "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")

openai.api_kEY = KEY
os.environ["OPENAI_API_KEY"] = KEY


class Retrievers:
    """
    Retrievers class handles querying the index with a given question to retrieve relevant responses.

    Args:
        top_k (int): Number of top results to retrieve.
        similarity_threshold (float): Similarity threshold for the retrieval results.

    """

    def __init__(self, config: RetrieversConfig):
        self.top_k = config.top_k
        self.similarity_threshold = config.similarity_threshold

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
        retriever = VectorIndexRetriever(
            index=index,
            similarity_top_k=self.top_k,
        )

        # Assemble the retriever query engine with the similarity postprocessor
        query_engine = RetrieverQueryEngine(
            retriever=retriever,
            node_postprocessors=[
                SimilarityPostprocessor(
                    similarity_cutoff=self.similarity_threshold)
            ]
        )

        # Perform the query and retrieve the response
        response = query_engine.query(question)
        return response.response
