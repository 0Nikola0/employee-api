import os

from dotenv import load_dotenv

load_dotenv(override=True)

BASE_URL    = os.environ["API_BASE_URL"]
CLIENT_ID   = os.environ["API_CLIENT_ID"]
CLIENT_SECRET = os.environ["API_CLIENT_SECRET"]
USERNAME    = os.environ["API_USERNAME"]
PASSWORD    = os.environ["API_PASSWORD"]
DATABASE_URL = os.environ["DATABASE_URL"]
