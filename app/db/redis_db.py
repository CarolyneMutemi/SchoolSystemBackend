"""
Redis client.
"""
from redis import Redis


redis_client = Redis()
if redis_client.ping():
    print("Redis connected.")
else:
    print("Redis not connected.")
