# app/__init__.py
from flask import Flask
from azure.cosmos import CosmosClient
from .routes import app as routes_app
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()


def create_app():
    app = Flask(__name__, template_folder="templates", static_folder="static")
    app.config["AOAI_COMPLETION_DEPLOYMENT"] = os.getenv("AOAI_COMPLETION_DEPLOYMENT")
    app.config["AOAI_KEY"] = os.getenv("AOAI_KEY")
    app.config["AOAI_ENDPOINT"] = os.getenv("AOAI_ENDPOINT")
    app.config["API_VERSION"] = "2024-02-01"

    app.register_blueprint(routes_app)

    return app
