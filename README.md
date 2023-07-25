# Chatgpt Long Term Memory

The ChatGPT Long Term Memory package is a powerful tool designed to empower your projects with the ability to handle a large number of simultaneous users. It achieves this by seamlessly integrating an extensive knowledge base and adaptive memory through cutting-edge technologies such as GPT from OpenAI, llama vector index, and Redis datastore. With this comprehensive set of capabilities, you can create highly scalable applications that provide contextually relevant and engaging conversations, enhancing the overall user experience and interaction.


## Key Features:

1. **Scalability**: The ChatGPT Long Term Memory package is designed to handle numerous concurrent users efficiently, making it suitable for applications with high user demand.

2. **Extensive Knowledge Base**: Benefit from the integration of a knowledge base that allows you to incorporate personalized data in the form of TXT files. This feature enables the system to provide contextually relevant responses and engage in meaningful conversations.

3. **Adaptive Memory**: The package utilizes cutting-edge technologies like GPT, llama vector index, and Redis datastore to ensure an adaptive memory system. This capability enables improved performance and coherent interactions, making the conversations more natural and engaging.

4. **Flexible Integration with GPT Models**: The package allows seamless interaction with GPT models, giving you the option to chat with GPT models using context memory. This enables you to engage with state-of-the-art language models for more advanced language processing tasks.

5. **Easy Setup and Configuration**: The package provides simple installation steps using `pip`, and you can quickly set up your environment with your API key from OpenAI. The configuration options are customizable, allowing you to tailor the package to suit your specific project requirements.

6. **Utilization of Redis Datastore**: The integration with Redis datastore ensures efficient data storage and retrieval, contributing to the overall scalability and responsiveness of the system.

7. **API Integration with OpenAI**: The package leverages the API from OpenAI to power its GPT-based functionalities. This ensures access to the latest advancements in language processing and capabilities of GPT models.

8. **Continuous Learning and Improvement**: As a GPT-based system, the ChatGPT Long Term Memory package benefits from continuous learning and improvement, staying up-to-date with the latest developments in language understanding and generation.

9. **Customizable Conversation Flow**: The package offers customizable conversation flows with the ability to include the user's chat history and knowledge base data. This enhances the contextual understanding and relevance of responses.

10. **Easy-to-Use Interfaces**: The provided code snippets and interfaces make it easy for developers to integrate the ChatGPT Long Term Memory package into their projects, minimizing the learning curve and streamlining the development process.

The combination of these key features makes the ChatGPT Long Term Memory package a valuable addition to your projects, allowing you to create interactive and dynamic conversational applications with powerful language processing capabilities.


# Getting Started:

To utilize the Chatgpt Long Term Memory package in your projects, follow the steps below:

    1. Install the package
    ```
    pip install chatgpt_long_term_memory
    ```
    2. Sign up and obtain your API kEY from [here](https://platform.openai.com/overview).
    3. Set OpenAI kEY in your env to access the ChatGPT service programmatically:
    ```
    export OPENAI_API_kEY=sk-******
    ```
    4. Customize the configuration and parameters to suit your project's needs.

# Example Usage:

pull redis docker image and run:
```
docker pull redis

docker network create --subnet=172.0.0.0/16 mynet123

docker run --name redis-db -d  --net mynet123 --ip 172.0.0.22 -p 6379:6379 -p 8001:8001 redis:latest

```

### Method 1: Utilizing Index Memory with Optional Knowledge Base
You can leverage index memory by setting knowledge_base=True to incorporate your personalized data in the form of TXT files located within the directory: {your_root_path}/resources/data. Ensure the proper addressing of the resources/data directory for seamless access to the stored data.

```python
# example/usage_index_memory.py

from utils import get_project_root

from chatgpt_long_term_memory.conversation import ChatGPTClient
from chatgpt_long_term_memory.llama_index_helpers import (IndexConfig,
                                                          RetrieversConfig)
from chatgpt_long_term_memory.memory import ChatMemoryConfig


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

```

### Method 2: Chat with GPT Models using Context Memory
In this scenario, you can't use your own database, but you can interact with the GPT models and use context memory.

```python
# example/usage_context_memory.py

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

```
