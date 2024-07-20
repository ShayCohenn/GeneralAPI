import redis
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from core.config import Setup

_client = MongoClient(Setup.MONGODB_URI, server_api=ServerApi('1'))
users_db = _client['users']['users']

redis_client = redis.Redis(
  host=Setup.REDIS_URL,
  port=Setup.REDIS_PORT,
  password=Setup.REDIS_PASSWORD)