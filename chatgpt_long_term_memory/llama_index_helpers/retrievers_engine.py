import os

import openai
from llama_index.indices.postprocessor import SimilarityPostprocessor
from llama_index.query_engine import RetrieverQueryEngine
from llama_index.retrievers import VectorIndexRetriever

kEY = os.getenv("OPENAI_API_KEY",
                "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")

openai.api_key = kEY
os.environ["OPENAI_API_KEY"] = kEY

class Retrievers:
    """
    Retrievers class handles querying the index with a given question to retrieve relevant responses.

    Args:
        top_k (int): Number of top results to retrieve.
        similarity_threshold (float): Similarity threshold for the retrieval results.

    """

    def __init__(self, top_k: int = 3, similarity_threshold: float = 0.7):
        self.top_k = top_k
        self.similarity_threshold = similarity_threshold

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
