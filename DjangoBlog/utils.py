import logging # 用于日志
import os
import random
import string
import uuid # 用于生成唯一标识符
from hashlib import sha256 # 用于加密

from django.core.cache import cache
from django.contrib.sites.models import Site
from django.conf import settings
# from django.utils.cache import get_cache_key


# __name__：这样可以知晓是哪个模块生成了日志
logger = logging.getLogger(__name__)


# 加密
def get_sha256(str):
    m = sha256(str.encode('utf-8'))
    return m.hexdigest()


# 装饰器,expiration为设置缓存失效时间，默认为3分钟
def cache_decorator(expiration=3 * 60):
    def wrapper(func):
        def news(*args, **kwargs):
            try:
                view = args[0]
                # 感觉这个有问题，这个是一定会有异常的
                key = view.get_cache_key()
            except:
                key = None
            if not key:
                # 如果key为空，则创建新的key
                # 将对象返回为字符串形式，作为key
                unique_str = repr((func, args, kwargs))

                m = sha256(unique_str.encode('utf-8'))
                key = m.hexdigest()
            value = cache.get(key)
            if value is not None:
                if str(value) == '__default_cache_value__':
                    # cache默认的缓存值
                    return None
                else:
                    return value
            else:
                # value为空，先用日志记录，再设置value
                logger.debug(
                    'cache_decorator set cache:%s key:%s' %
                    (func.__name__, key))
                value = func(*args, **kwargs)
                if value is None:
                    cache.set(key, '__default_cache_value__')
                else:
                    cache.set(key, value, expiration)
                return value
        return news
    return wrapper
            

@cache_decorator
def get_current_site():
    # 获取站点的域名
    site = Site.objects.get_current()
    return site


def delete_sidebar_cache():
    from blog.models import LinkShowType
    keys = ["sidebar" + x for x in LinkShowType.values]
    for k in keys:
        logger.info('delete sidebar key:' + k)
        cache.delete(k)



