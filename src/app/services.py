import os
from azure.cosmos import CosmosClient, PartitionKey, exceptions
from openai import AzureOpenAI

API_VERSION = '2024-02-01'

class AIService:
    def __init__(self):
        self.endpoint = os.environ.get('AOAI_ENDPOINT')
        self.key = os.environ.get('AOAI_KEY')
        self.client = AzureOpenAI(
            azure_endpoint=self.endpoint,
            api_key=self.key,
            api_version=API_VERSION
        )
  
    def get_completion(self, prompt):
        try:
            completion = self.client.chat.completions.create(
            model=os.environ.get('AOAI_COMPLETION_DEPLOYMENT'),
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                max_tokens=800,
                temperature=0.7,
                top_p=0.95,
                frequency_penalty=0,
                presence_penalty=0,
                stop=None,
                stream=False
            )
            return completion.choices[0].message.content
        except Exception as e:
            print(f"Error getting completion: {e}")
            return "An error occurred while generating a response."