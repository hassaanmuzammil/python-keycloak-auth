import os
import urllib.parse
from dotenv import load_dotenv

# Load environment variables
load_dotenv(override=True)

# start .env
KEYCLOAK_SERVER_URL = os.environ.get("KEYCLOAK_SERVER_URL")
KEYCLOAK_REALM = os.environ.get("KEYCLOAK_REALM")
KEYCLOAK_CLIENT_ID = os.environ.get("KEYCLOAK_CLIENT_ID")
KEYCLOAK_CLIENT_SECRET = os.environ.get("KEYCLOAK_CLIENT_SECRET")
KEYCLOAK_ADMIN = os.environ.get("KEYCLOAK_ADMIN")
KEYCLOAK_ADMIN_PASSWORD = os.environ.get("KEYCLOAK_ADMIN_PASSWORD")
DB_HOST = os.environ.get("DB_HOST")
DB_PORT = os.environ.get("DB_PORT")
DB_NAME = os.environ.get("DB_NAME")
DB_USER = os.environ.get("DB_USER")
DB_PASSWORD = urllib.parse.quote(os.environ.get("DB_PASSWORD"))
# end .env