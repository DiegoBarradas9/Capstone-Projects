from flask import Flask, send_from_directory
from flask_cors import CORS
from app.blueprint import ApiBlueprint
from dotenv import load_dotenv
import sys
import os

load_dotenv()

def testFunction():
  import data.automation.eventTableMigrator

if __name__ == "__main__":
  if ("--init" in sys.argv):
    import app.database.tableInitializer
    exit()
  if ("--test" in sys.argv):
    testFunction()
    exit()
  if ("--reset" in sys.argv):
    if (os.path.isfile(os.getenv("DB_PATH"))):
      os.remove(os.getenv("DB_PATH"))
    exit()

  Server = Flask(__name__)
  CORS(Server, resources={r"/*": {
    "origins": "*",
    "allow_headers": "*",
    "methods": ["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
    "supports_credentials": True
  }})

  @Server.route("/uploads/<path:path>")
  def staticFileHost(path):
    return send_from_directory("uploads", path)

  Server.register_blueprint(ApiBlueprint)
  Server.run(host="localhost", port=8000)