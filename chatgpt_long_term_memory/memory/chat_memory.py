from datetime import datetime

from redis_chatgpt.manager import RedisManager

from chatgpt_long_term_memory.memory.config import ChatMemoryConfig


class ChatMemory:
    """
    Create a straightforward chat history storage solution using the llama index and Redis for efficient buffering.

    Args:
        redis_host (str): Host address of the Redis server.
        redis_port (int): Port number of the Redis server.

    """

    def __init__(self, memory_config: ChatMemoryConfig, **kw):
        super().__init__(**kw)
        self.config = memory_config
        self.redis_db = RedisManager(
            host=self.config.redis_host, port=self.config.redis_port)

    def get(self, user_id):
        """
        Retrieve the chat history for a specific user from Redis.

        Args:
            user_id (str): Unique identifier for the user.

        Returns:
            list: List of dictionaries representing the user's chat history.
        """
        redis_key = f"{user_id}_data"
        retrieved_documents = self.redis_db.get_data(redis_key)
        return retrieved_documents

    def add_conversation(self, user_id: str, conversation: tuple):
        """
        Add a new conversation to the user's chat history in Redis.

        Args:
            user_id (str): Unique identifier for the user.
            conversation (tuple): A tuple containing the user's question and the bot's response.

        """
        redis_key = f"{user_id}_data"
        data = {
            f"{datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')}": {
                "user_query": conversation[0],
                "bot_response": conversation[1]
            }
        }
        try:
            # Retrieve the existing chat history for the user from Redis
            history = self.redis_db.get_data(redis_key)
            history.append(data)
        except Exception as e:
            # If no existing chat history is found, create a new list with the current conversation data
            history = [data]
        # Update the user's chat history in Redis
        self.redis_db.set_data(redis_key, history)
