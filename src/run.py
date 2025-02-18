import os
from app.routes import app

print(f"FLASK_ENV: {os.getenv('FLASK_ENV')}")
print(f"FLASK_DEBUG: {os.getenv('FLASK_DEBUG')}")

# app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
