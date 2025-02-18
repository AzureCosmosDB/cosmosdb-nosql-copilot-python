from flask import Flask
from azure.cosmos import CosmosClient
from routes import app as routes_blueprint
# from .config import Config


app = Flask(__name_,  
            template_folder='templates',
            static_folder='static'
)

# Register the blueprint from routes.py
app.register_blueprint(routes_blueprint)


# Initialize Cosmos DB Client
client = CosmosClient(Config.COSMOS_ENDPOINT, credential=Config.COSMOS_KEY)
database = client.get_database_client(Config.COSMOS_DATABASE)

if __name__ == '__main__':
    app.run(debug=True)
    
    
    
    
    
# # Example function to create a container
# def create_container(container_name):
#     try:
#         database.create_container(id=container_name, partition_key='/id', offer_throughput=400)
#         print(f'Container {container_name} created.')
#     except Exception as e:
#         print(f'Error creating container: {e}')
        
        
# # Function to create an item
# def create_item(container_name, item):
#     container = database.get_container_client(container_name)
#     container.upsert_item(item)
#     print(f'Item {item} created/updated in {container_name}.')

# # Function to read an item
# def read_item(container_name, item_id):
#     container = database.get_container_client(container_name)
#     item = container.read_item(item_id, partition_key=item_id)
#     return item