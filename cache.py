from araplus.settings import CACHE_URL, CACHE_SERVICE_CODE
from arcus import *
from arcus_mc_node import ArcusMCNodeAllocator

_cache = None

def get_cache():
    global _cache
    if not _cache:
        print 'cache server start!'
        _cache = Arcus(ArcusLocator(ArcusMCNodeAllocator(ArcusTranscoder())))
        _cache.connect(CACHE_URL, CACHE_SERVICE_CODE)
    return _cache

def set(key, value, time=10):
    c = get_cache()
    c.set(key, value, time)

def get(key):
    c = get_cache()
    return c.get(key).get_result()
