from sqlmodel import create_engine, text
from dotenv import load_dotenv
import os
from pathlib import Path

load_dotenv(Path("/Users/paulzpaulus/Desktop/Masterschool/Flashme/flashMe/.env"))

DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL not set")

engine = create_engine(DATABASE_URL, echo=True)

with engine.connect() as conn:
    result = conn.execute(text("SELECT 1")) # type: ignore
    print("OK:", result.scalar()) # type: ignore
