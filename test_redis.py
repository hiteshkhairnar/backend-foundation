from app.database.redis import redis_client

redis_client.set("message", "Hello Redis")

print(redis_client.get("message"))