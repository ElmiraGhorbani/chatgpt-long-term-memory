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

# root path that contains resource data
root_path = get_project_root()
doc_indexer_config = IndexConfig(root_path=f"{root_path}/chatgpt-long-term-memory/example/chatbot", knowledge_base=False)
retrievers_config = RetrieversConfig()
chat_memory_config = ChatMemoryConfig(
    redis_host="172.0.0.22",
    redis_port=6379
)
chatgpt_client = ChatGPTClient(doc_indexer_config=doc_indexer_config, retrievers_config=retrievers_config, chat_memory_config=chat_memory_config)

print(chatgpt_client.converse("hi", '1'))
