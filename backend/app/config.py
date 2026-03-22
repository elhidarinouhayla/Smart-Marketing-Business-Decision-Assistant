from dotenv import load_dotenv
import os

from pathlib import Path
env_path = Path(__file__).parent / ".env"
load_dotenv(dotenv_path=env_path)


USER=os.getenv("USER")
PASSWORD=os.getenv("PASSWORD")
PORT=os.getenv("PORT")
HOST=os.getenv("HOST")
DATABASE=os.getenv("DATABASE")



SECRET_KEY=os.getenv("SECRET_KEY")
ALGORITHM=os.getenv("ALGORITHM")


GEMINI_API_KEY=os.getenv("GEMINI_API_KEY")