import redis
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from core.config import MongoDBConfig, RedisConfig

_client = MongoClient(MongoDBConfig.MONGODB_URI, server_api=ServerApi('1'))
users_db = _client['users']['users']
cities_collection = _client['Locations']['Cities']
countries_collection = _client['Locations']['Countries']

redis_client = redis.Redis(
  host=RedisConfig.REDIS_URL,
  port=RedisConfig.REDIS_PORT,
  password=RedisConfig.REDIS_PASSWORD)