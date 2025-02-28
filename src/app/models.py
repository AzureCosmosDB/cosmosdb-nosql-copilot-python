import uuid
from datetime import datetime, timezone
from azure.cosmos import CosmosClient, PartitionKey, exceptions
from .config import Config
from .services import AIService


# Initialize Cosmos DB Client
client = CosmosClient(Config.COSMOS_ENDPOINT, credential=Config.COSMOS_KEY)
database = client.create_database_if_not_exists(Config.COSMOS_DATABASE)
container = database.create_container_if_not_exists(
    "chat", partition_key=PartitionKey("/id")
)
cache_container = database.create_container_if_not_exists(
    "cache", partition_key=PartitionKey("/id")
)



# Message Model
class Message:
    """A Message is defined by a unique ID, a session ID, a prompt, and a completion."""

    def __init__(
        self, session_id, prompt, prompt_tokens=0, completion="", completion_tokens=0
    ):
        self.id = str(uuid.uuid4())
        self.session_id = session_id
        self.timestamp = datetime.now(timezone.utc).isoformat()
        self.prompt = prompt
        self.prompt_tokens = prompt_tokens
        self.completion = completion
        self.completion_tokens = completion_tokens

    def __str__(self):
        return f"Message {self.id} in Session {self.session.id} - Prompt: {self.prompt[:50]}"

    def save(self):
        item = {
            "id": self.id,
            "session_id": self.session_id,
            "timestamp": self.timestamp,
            "prompt": self.prompt,
            "prompt_tokens": self.prompt_tokens,
            "completion": self.completion,
            "completion_tokens": self.completion_tokens,
            "type": "message",
        }

        # Save to Cosmos DB
        try:
            container.upsert_item(item)
            print(f"Message {self.id} saved to Cosmos DB.")
        except Exception as e:
            print(f"Error saving Message {self.id}: {e}")

        cache = CacheItem(self)
        cache.save()
        
    def generate_completion(self):
        ai_service = AIService()
        self.completion = ai_service.get_completion(self.prompt)
        self.completion_tokens = len(self.completion.split())


# Session Model
class ChatSession:
    """A Session is defined by a unique ID and a name, and it contains multiple messages and keeps track of the total token count."""

    def __init__(self, session_id=None, tokens=None, session_name="New Chat"):
        self.session_id = session_id or str(uuid.uuid4())
        self.tokens = tokens or 0
        self.session_name = session_name
        self.container = database.create_container_if_not_exists(
            "chat", partition_key=PartitionKey("/id")
        )

    def __str__(self):
        return f"Session {self.session_id} - {self.session_name}"

    def add_message(self, prompt, prompt_tokens, completion="", completion_tokens=0):
        """Add a message to the Session and update the token count."""
        message = Message(
            session_id=self.session_id,
            prompt=prompt,
            prompt_tokens=prompt_tokens,
            completion=completion,
            completion_tokens=completion_tokens,
        )
        message.save()

        # Update session tokens
        self.tokens += prompt_tokens + completion_tokens
        self.save()  # Save the session after updating tokens

    @staticmethod
    def get_all_sessions():
        """Get all sessions from the database."""
        query = "SELECT DISTINCT c.id, c.name FROM c WHERE IS_DEFINED(c.name)"
        sessions = list(container.query_items(query, enable_cross_partition_query=True))
        return sessions
    
    def get_messages(self):
        """Get all messages for this session."""
        query = "SELECT c.session_id, c.prompt, c.completion, c.completion_tokens, c.prompt_tokens FROM c WHERE c.session_id = @session_id"
        parameters = [{"name": "@session_id", "value": self.session_id}]
        messages = list(container.query_items(query, parameters=parameters, enable_cross_partition_query=True))
        return [Message(**message) for message in messages]


    def save(self):
        # Create a session item to save
        session_item = {
            "id": self.session_id,
            "tokens": self.tokens,
            "name": self.session_name,
            "type":"session",
        }

        # Insert or update the session item in the container
        try:
            self.container.create_item(session_item)  # Create a new session item
        except exceptions.CosmosHttpResponseError as e:
            # If the item already exists, you might want to update it
            if e.status_code == 409:  # Conflict
                self.container.upsert_item(session_item)  # Upsert (insert or update)

# CacheItem Model
class CacheItem(Message):
    pass

    def __init__(self, message,vectors=None):
        super().__init__(message.session_id, message.prompt, message.completion)
        self.vectors = vectors
        self.id = str(uuid.uuid4())


    def save(self):
        """Store completions in the cache"""
        item = {
            "id": self.id, 
            "message_id": self.id,
            "session_id": self.session_id,
            "vectors": self.vectors,
            "prompt": self.prompt,
            "completion": self.completion,
        }

        # Save to Cosmos DB
        try:
            cache_container.upsert_item(item)
            print(f"CacheItem {self.id} saved to Cosmos DB.")
        except Exception as e:
            print(f"Error saving CacheItem {self.id}: {e}")

    def clear_cache(self):
        """Clear the cache"""
        try:
            for item in cache_container.query_items(
                query="SELECT * FROM c",
                enable_cross_partition_query=True,
            ):
                cache_container.delete_item(item)
            print(f"CacheItem {self.id} cleared from Cosmos DB.")

        except Exception as e:
            print(f"Error clearing CacheItem {self.id}: {e}")

    def __str__(self):
        return f"CacheItem {self.id} - Prompt: {self.prompts[:50]}"


    # def check_cache(prompt):
    #     return CacheItem.objects.filter(prompts=prompt).first()
