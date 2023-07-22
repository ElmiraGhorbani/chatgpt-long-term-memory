# Chatgpt Long Term Memory

The Chatgpt Long Term Memory package is designed to empower your projects by accommodating a large number of simultaneous users while leveraging an extensive knowledge base and adaptive memory. This capability is made possible through the integration of cutting-edge technologies, including GPT(OpenAI), llama vector index, and Redis datastore.

## KEY Features:

- Scalability to handle numerous concurrent users
- Access to an expansive knowledge base
- Adaptive memory for improved performance
- Powered by state-of-the-art technologies like GPT, llama vector index, and Redis datastore

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

```
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
doc_indexer_config = IndexConfig(root_path=root_path)
retrievers_config = RetrieversConfig()
chat_memory_config = ChatMemoryConfig()
chatgpt_client = ChatGPTClient(doc_indexer_config=doc_indexer_config, retrievers_config=retrievers_config, chat_memory_config=chat_memory_config)

print(chatgpt_client.converse("hi", '1'))
```