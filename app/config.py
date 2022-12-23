import os 
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.environ.get("MONGO_URI")

JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY")

JWT_ALGORITHM = os.environ.get("JWT_ALGORITHM")