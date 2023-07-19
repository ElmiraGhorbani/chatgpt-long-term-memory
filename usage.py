import os

from chatgpt_long_term_memory.conversation import ChatGPTClient
from chatgpt_long_term_memory.llama_index_helpers.config import (
    IndexConfig, RetrieversConfig)
from chatgpt_long_term_memory.memory.config import ChatMemoryConfig


def get_project_root():
    # Get the absolute path of the current file
    current_path = os.path.abspath(__file__)
    # Return the parent directory (project root)
    return os.path.dirname(os.path.dirname(current_path))


root_path = get_project_root()
doc_indexer_config = IndexConfig(root_path=root_path,
                                 knowledge_base=True,  # Set this to True or False based on whether the user has a personal knowledge base.
                                 model_name="gpt-3.5-turbo",
                                 temperature=0,
                                 context_window=4096,
                                 num_outputs=700,
                                 max_chunk_overlap=0.5,
                                 chunk_size_limit=600)
retrievers_config = RetrieversConfig()
chat_memory_config = ChatMemoryConfig()
chatgpt_client = ChatGPTClient(doc_indexer_config=IndexConfig,
                               retrievers_config=retrievers_config, chat_memory_config=chat_memory_config)

print(chatgpt_client.converse('hi', '1'))
