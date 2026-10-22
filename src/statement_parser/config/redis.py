from redis import Redis

from statement_parser.config.settings import settings

redis_client = Redis.from_url(settings.redis_url, socket_timeout=2)
