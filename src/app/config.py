from azure.cosmos import CosmosClient, PartitionKey, exceptions
from openai import AzureOpenAI
import os


class Config:
    COSMOS_ENDPOINT = os.environ.get('COSMOS_ENDPOINT', 'your-cosmos-db-endpoint')
    COSMOS_KEY = os.environ.get('COSMOS_KEY', 'your-cosmos-db-key')
    COSMOS_DATABASE = os.environ.get('COSMOS_DATABASE', 'CosmosCopilotPythonDB')
    AOAI_COMPLETION_DEPLOYMENT = os.environ.get('AOAI_COMPLETION_DEPLOYMENT')
    AOAI_KEY = os.environ.get('AOAI_KEY')
    AOAI_ENDPOINT = os.environ.get('AOAI_ENDPOINT')
    API_VERSION = '2024-02-01'