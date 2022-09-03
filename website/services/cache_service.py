"""Cache manager"""
from flask_caching import Cache


class CacheService:
    """Cache manager"""

    def __init__(self):
        self._cache = Cache(config={"CACHE_TYPE": "SimpleCache"})

    def init_cache(self, app):
        self._cache.init_app(app)

    def get_cache(self):
        return self._cache
