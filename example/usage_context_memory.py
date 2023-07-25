from utils import get_project_root

from chatgpt_long_term_memory.conversation import ChatbotClient
from chatgpt_long_term_memory.llama_index_helpers import (IndexConfig,
                                                          RetrieversConfig)
from chatgpt_long_term_memory.memory import ChatMemoryConfig
from chatgpt_long_term_memory.openai_engine import OpenAIChatConfig


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

# Method 2: chat with gpt models, use context memory in this scenario you can't use your own db
openai_chatbot_config = OpenAIChatConfig(
    model_name="gpt-4",
    max_tokens=1000,
    temperature=0,
    top_p=1,
    presence_penalty=0,
    frequency_penalty=0,
    # keep in mind if you change prompt, consider history and human input
    prompt="""Assistant is a large language model trained by OpenAI.

    Assistant is designed to be able to assist with a wide range of tasks, from answering simple questions to providing in-depth explanations and discussions on a wide range of topics. As a language model, Assistant is able to generate human-like text based on the input it receives, allowing it to engage in natural-sounding conversations and provide responses that are coherent and relevant to the topic at hand.

    Assistant is constantly learning and improving, and its capabilities are constantly evolving. It is able to process and understand large amounts of text, and can use this knowledge to provide accurate and informative responses to a wide range of questions. Additionally, Assistant is able to generate its own text based on the input it receives, allowing it to engage in discussions and provide explanations and descriptions on a wide range of topics.

    Overall, Assistant is a powerful tool that can help with a wide range of tasks and provide valuable insights and information on a wide range of topics. Whether you need help with a specific question or just want to have a conversation about a particular topic, Assistant is here to assist.

    History: {}
    Human: {}
    Assistant:"""
)

# Initialize the chatbot client.

chat_app = ChatbotClient(
    doc_indexer_config=doc_indexer_config,
    retrievers_config=retrievers_config,
    chat_memory_config=chat_memory_config,
    openai_chatbot_config=openai_chatbot_config
)

# Start a conversation with the user.

user_id = 2

while True:

    # Get the user's input.
    user_input = input("User Input:")

    # If the user enters "q", break out of the loop.
    if user_input == "q":
        break

    # Get the response from the chatbot.
    index, response = chat_app.converse(user_input, user_id=user_id)

    # Print the response to the user.
    print(response)
