#__init__.py

from flask import Flask
import os
from dotenv import load_dotenv

def create_app():
    load_dotenv()

    # Explicitly tell Flask to use root-level "templates" folder
    app = Flask(__name__, template_folder="../templates")

    from .memory import LongTermMemory
    LongTermMemory.init_memory()

    from .routes import register_routes
    register_routes(app)

    return app
