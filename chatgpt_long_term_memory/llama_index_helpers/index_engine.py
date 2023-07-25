import os
import uuid

import openai
from llama_index import (Document, PromptHelper, ServiceContext,
                         SimpleDirectoryReader, StorageContext,
                         VectorStoreIndex, load_index_from_storage,
                         set_global_service_context)
from llama_index.llms import OpenAI

from chatgpt_long_term_memory.llama_index_helpers.config import IndexConfig

# Set the OpenAI API kEY using the environment variable or a default kEY
KEY = os.getenv("OPENAI_API_KEY",
                "")
openai.api_key = KEY
os.environ["OPENAI_API_KEY"] = KEY


class DocIndexer:
    """
    DocIndexer class can help to create an index from a knowledge base and user's query and chatbot response.

    Args:
        root_path (str): Root path for the storage of indices and data.
        knowledge_base (bool): Boolean flag indicating whether the user has a personal knowledge base.
        model_name (str): Name of the language model to use (e.g., "gpt-3.5-turbo").
        temperature (int): Temperature for language model sampling.
        context_window (int): Context window for the LLM.
        num_outputs (int): Number of outputs for the LLM.
        max_chunk_overlap (float): Chunk overlap as a ratio of chunk size.
        chunk_size_limit (Optional[int]): Maximum chunk size to use.

    """

    def __init__(
            self, doc_config: IndexConfig, **kw):
        super().__init__(**kw)
        self.config = doc_config

        # Initialize the OpenAI language model
        self.llm = OpenAI(model=self.config.model_name,
                          temperature=self.config.temperature)
        service_context = ServiceContext.from_defaults(llm=self.llm)
        set_global_service_context(service_context)

        self.root_path = self.config.root_path
        if self.config.knowledge_base:
            self.data_path = f'{self.root_path}/resources/data'
            assert os.path.exists(
                self.data_path), f"Path '{self.data_path}' does not exist!"

        # Define prompt helper for the index
        self.prompt_helper = PromptHelper(
            self.config.context_window,
            self.config.num_outputs,
            self.config.max_chunk_overlap,
            chunk_size_limit=self.config.chunk_size_limit
        )

    def load_documents(self, retrieved_documents):
        """
        Load and create a generic interface for a data document from retrieved chat history.

        Args:
            retrieved_documents (list): List of dictionaries containing user's chat history.

        Returns:
            Document: A document object representing the chat history.
        """
        # Sort the dictionaries based on the date strings
        sorted_data = sorted(retrieved_documents,
                             key=lambda x: list(x.keys())[0], reverse=True)
        doc = list(sorted_data[0].values())[0]
        doc = f"USER: {doc['user_query']}, ANSWER: {doc['bot_response']}"
        return Document(text=doc, doc_id=f"doc_id_{str(uuid.uuid4())}")

    def construct_index_general(self, user_id, path, mode):
        """
        Construct and persist the index for a specific user.

        Args:
            user_id (str): Unique identifier for the user.
            path (str): Path to store the user's index.
            mode (str): Mode for constructing the index, either "kb" (knowledge base) or "user" (user input).

        Returns:
            VectorStoreIndex: The constructed index.
        """
        # If the user's storage directory does not exist, create it.
        if not os.path.exists(path):
            os.makedirs(path)

        # Load data from the directory for the user's personal knowledge base
        if mode == 'kb':
            if self.config.knowledge_base:
                documents = SimpleDirectoryReader(self.data_path).load_data()
            else:
                # User doesn't have any personal knowledge base
                documents = []

        # Create a Document structure for the user's input query and chatbot response
        if mode == 'user':
            documents = [self.load_documents(user_id)]

        # Construct index
        index = VectorStoreIndex.from_documents(
            documents, prompt_helper=self.prompt_helper
        )

        # Persist index
        index.storage_context.persist(path)

        if mode == 'kb':
            return index

    def load_index(self, user_id):
        """
        Load the user's index from storage or construct a new one if not found.

        Args:
            user_id (str): Unique identifier for the user.

        Returns:
            VectorStoreIndex: The loaded or newly constructed index.
        """
        index_path = f'{self.root_path}/storages/storage_{user_id}'
        status = os.path.exists(f'{index_path}/vector_store.json')
        if status:
            index = load_index_from_storage(
                StorageContext.from_defaults(persist_dir=index_path))
        else:
            index = self.construct_index_general(
                user_id, index_path, mode="kb")
        return index

    def update_index(self, user_id, index, retrieved_documents):
        """
        Update the user's index with new chat history and persist the changes.

        Args:
            user_id (str): Unique identifier for the user.
            index (VectorStoreIndex): The user's index.
            retrieved_documents (list): List of dictionaries containing user's chat history.

        """
        path = f'{self.root_path}/storages/storage_{user_id}'
        doc = self.load_documents(retrieved_documents)
        index.insert(doc)
        index.storage_context.persist(path)
