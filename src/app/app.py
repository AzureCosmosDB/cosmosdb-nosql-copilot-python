from flask import Flask
from .routes import app as routes_blueprint
from .config import Config

print("Starting app.py")  # Debug print


app = Flask(__name__,  
            template_folder='templates',
            static_folder='static'
)

app.secret_key = Config.SECRET_KEY

# Register the blueprint from routes.py
app.register_blueprint(routes_blueprint)


if __name__ == '__main__':
    app.run(debug=True)
