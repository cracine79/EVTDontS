import sys
import os

# Ensure the backend folder is in the Python path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from backend.main import create_app
from backend.config import DevConfig

if __name__=='__main__':
    app=create_app(DevConfig)
    app.run(host="0.0.0.0", port=3000)