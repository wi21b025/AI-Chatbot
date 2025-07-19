import os
from dotenv import load_dotenv

dotenv_path = os.path.join('config', '.env')
load_dotenv(dotenv_path)
CHROMA_PATH = "data/books/test/chroma"
DATA_PATH = "data/books"
LINKS_JSON_PATH = "data/links/links.json"
# Retrieve the API key from the environment
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
if not OPENAI_API_KEY:
    raise ValueError("No OpenAI API key found. Please set it in your .env file.")
