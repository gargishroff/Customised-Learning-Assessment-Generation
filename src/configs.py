"""
Here we store a couple of common config variables used by the entire codebase
"""

import os
from pathlib import Path

from dotenv import load_dotenv
from flask_pymongo import PyMongo

load_dotenv()

CODE_BASE = Path(__file__).resolve().parent
FRONTEND_BASE = CODE_BASE / "my-app"
FRONTEND_BUILD = FRONTEND_BASE / "build"

UPLOADS_BASE = CODE_BASE / "uploads"
ALLOWED_EXTENSIONS = {".pdf"}
ALLOWED_MIMETYPES = {"application/pdf"}

LLM_TIMEOUT = int(os.environ.get("LLM_TIMEOUT", "300"))
API_TOKEN = os.environ["API_TOKEN"]
API_URL = (
    "https://api-inference.huggingface.co/models/mistralai/Mixtral-8x7B-Instruct-v0.1"
)

MONGO_URI = os.environ["MONGO_URI"]

# app.py sets this parameter so that they can be used across the codebase
pymongo: PyMongo | None = None
