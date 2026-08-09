from datetime import datetime,timedelta
class CacheService:
    def __init__(self):
        self._cache={}
    async def get(self,key):
        item=self._cache.get(key)
        if not item:return None
        if item["expires"]<datetime.utcnow():
            self._cache.pop(key,None); return None
        return item["value"]
    async def set(self,key,value,ttl=300):
        self._cache[key]={"value":value,"expires":datetime.utcnow()+timedelta(seconds=ttl)}
