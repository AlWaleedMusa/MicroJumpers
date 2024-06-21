from django.core.cache import cache
from storages.backends.dropbox import DropboxStorage

class CachedDropboxStorage(DropboxStorage):

    def url(self, name):
        cached_url = cache.get(name)
        if cached_url:
            print("cashed")
            return cached_url

        url = super().url(name)
        cache.set(name, url, timeout=60*5)
        print("not chached")
        return url
