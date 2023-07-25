from utils import get_project_root

from chatgpt_long_term_memory.conversation import ChatGPTClient
from chatgpt_long_term_memory.llama_index_helpers import (IndexConfig,
                                                          RetrieversConfig)
from chatgpt_long_term_memory.memory import ChatMemoryConfig

"""
Method 1: Utilizing Index Memory with Optional Knowledge Base

You can leverage index memory by setting knowledge_base=True to 
incorporate your personalized data in the form of TXT files located within the directory: {your_root_path}/resources/data.
It is essential to address the resources/data directory to ensure seamless access to the data stored therein.
"""

# Get project's root path
root_path = get_project_root()

"""
First: 
Initialize llama indexes config to create a index from knowledge base and user's chat history.
The root_path specifies the directory where the index will be stored.
The knowledge_base flag specifies whether to index the knowledge base.
The model_name specifies the name of the language model to use for indexing.
The temperature parameter controls the randomness of the output.
The context_window parameter specifies the size of the context window to use for indexing.
The num_outputs parameter specifies the number of output tokens to generate for each input token.
The max_chunk_overlap parameter specifies the maximum overlap between chunks.
The chunk_size_limit parameter specifies the maximum size of a chunk.
"""
doc_indexer_config = IndexConfig(
    root_path=f"{root_path}/example",
    knowledge_base=True,
    model_name="gpt-3.5-turbo",
    temperature=0,
    context_window=4096,
    num_outputs=700,
    max_chunk_overlap=0.5,
    chunk_size_limit=600
)

"""
Second:
# Initialize retrievers config to configure the retrievers class.

# The `top_k` parameter specifies the number of top-k documents to retrieve for each query.
# The `max_tokens` parameter specifies the maximum number of tokens to return for each document.
"""
retrievers_config = RetrieversConfig(
    top_k=7,
    max_tokens=1000
)

"""
Then:
Initialize chat memory config to configure the chat memory class.

The `redis_host` parameter specifies the hostname of the Redis server.
The `redis_port` parameter specifies the port of the Redis server.
"""
chat_memory_config = ChatMemoryConfig(
    redis_host="172.0.0.22",
    redis_port=6379
)

"""
Create a `ChatGPTClient` object to start the conversation.
The `doc_indexer_config` parameter specifies the configuration for the document indexer.
The `retrievers_config` parameter specifies the configuration for the retrievers.
The `chat_memory_config` parameter specifies the configuration for the chat memory.
"""

chatgpt_client = ChatGPTClient(
    doc_indexer_config=doc_indexer_config,
    retrievers_config=retrievers_config,
    chat_memory_config=chat_memory_config
)

# Start a conversation with the user.

user_id = 1

while True:

    # Get the user's input.
    user_input = input("User Input:")

    # If the user enters "q", break out of the loop.
    if user_input == "q":
        break

    # Get the response from the chatbot.
    index, response = chatgpt_client.converse(user_input, user_id=user_id)

    # Print the response to the user.
    print(response)
