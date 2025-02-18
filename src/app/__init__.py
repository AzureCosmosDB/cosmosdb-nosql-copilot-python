# app/__init__.py
from flask import Flask
from azure.cosmos import CosmosClient
from .routes import app as routes_app
from dotenv import load_dotenv
import os
 
# Load environment variables from .env file
load_dotenv()

def create_app():
    app = Flask(__name__)

    app.config['AOAI_COMPLETION_DEPLOYMENT'] = os.getenv('AOAI_COMPLETION_DEPLOYMENT')
    app.config['AOAI_KEY'] = os.getenv('AOAI_KEY')
    app.config['AOAI_ENDPOINT'] = os.getenv('AOAI_ENDPOINT')
    app.config['API_VERSION'] = '2024-02-01'

    # cosmos_client = CosmosClient(app.config['COSMOS_ENDPOINT'], app.config['COSMOS_KEY'])
    # database = cosmos_client.get_database_client(app.config['COSMOS_DATABASE'])
    # # container = database.get_container_client(app.config['COSMOS_CONTAINER'])

    # app.container = container
    # csrf.init_app(app)

    app.register_blueprint(routes_app)

    return app