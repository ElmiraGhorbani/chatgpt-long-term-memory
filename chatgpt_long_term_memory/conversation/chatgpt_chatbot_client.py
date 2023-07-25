# Import necessary classes from modules
from chatgpt_long_term_memory.llama_index_helpers.config import (
    IndexConfig, RetrieversConfig)
from chatgpt_long_term_memory.llama_index_helpers.index_engine import \
    DocIndexer
from chatgpt_long_term_memory.llama_index_helpers.retrievers_engine import \
    Retrievers
from chatgpt_long_term_memory.memory.chat_memory import ChatMemory
from chatgpt_long_term_memory.memory.config import ChatMemoryConfig
from chatgpt_long_term_memory.openai_engine.config import OpenAIChatConfig
from chatgpt_long_term_memory.openai_engine.openai_chatbot import OpenAIChatBot


class ChatbotClient(DocIndexer, Retrievers, ChatMemory, OpenAIChatBot):
    def __init__(self, doc_indexer_config: IndexConfig,
                 retrievers_config: RetrieversConfig,
                 chat_memory_config: ChatMemoryConfig,
                 openai_chatbot_config: OpenAIChatConfig):

        super().__init__(doc_config=doc_indexer_config, retrieve_config=retrievers_config,
                         memory_config=chat_memory_config, openai_chatbot_config=openai_chatbot_config)
    def converse_callback(self, question: str, user_id: str, callback=None):
        """
        This method performs a conversation with the ChatGPT client.

        Args:
            question (str): The user's question or input.
            user_id (str): Unique identifier for the user.
            callback (function, optional): A function to be called after the conversation. Defaults to None.

        Returns:
            tuple: A tuple containing the index and the response to the user's input.
        """
        # Load the index associated with the user
        index = self.load_index(user_id)

        # Query the index to get a response for the user's question
        nodes = self.get_nodes(question=question, index=index)

        query_response = self.chat(question, nodes)

        # Create a conversation tuple with the user's question and the response
        conversation = (question, query_response)

        # Add the conversation to the user's chat memory
        self.add_conversation(user_id, conversation)

        # Call the provided callback function with user_id and the updated index
        if callback:
            callback(user_id, index)

        # Return the index and the response
        return index, query_response

    def after_converse_callback(self, user_id: str, index):
        """
        This method updates the index for a user after a conversation.

        Args:
            user_id (str): Unique identifier for the user.
            index: The updated index to be stored for the user.
        """
        # Update the index for the user
        retrieved_documents = self.get(user_id)
        self.update_index(user_id, index, retrieved_documents)

    def converse(self, question: str, user_id: str):
        """
        This method initiates a conversation with the ChatGPT client.

        Args:
            question (str): The user's question or input.
            user_id (str): Unique identifier for the user.

        Returns:
            tuple: A tuple containing the index and the response to the user's input.
        """
        # Start the conversation by calling the converse_callback method
        # and passing the user's question, user_id, and after_converse_callback function
        index, query_response = self.converse_callback(
            question, user_id, self.after_converse_callback)

        # Return the index and the response
        return index, query_response
