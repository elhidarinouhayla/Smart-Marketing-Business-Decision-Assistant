from dotenv import load_dotenv
import os

load_dotenv()


USER=os.getenv("USER", "DB_User")
PASSWORD=os.getenv("PASSWORD", "DB_PASSWORD")
PORT=os.getenv("PORT",5432)
HOST=os.getenv("HOST", "db")
DATABASE=os.getenv("DATABASE", "DB_NAME")



SECRET_KEY=os.getenv("SECRET_KEY")
ALGORITHM=os.getenv("ALGORITHM")


GEMINI_API_KEY=os.getenv("GEMINI_API_KEY")