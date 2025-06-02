from dotenv import load_dotenv
import sqlite3
import os

load_dotenv()
DB_PATH = os.getenv("DB_PATH")

def cursorInstance():
  connect = sqlite3.connect(DB_PATH)
  return connect, connect.cursor()

