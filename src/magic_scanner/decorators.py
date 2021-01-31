import time
from weakref import WeakKeyDictionary


class reify:
    def __init__(self, method_to_reify):
        self._method = method_to_reify
        self._map = WeakKeyDictionary()
    
    def __get__(self, instance, owner=None):
        if instance is None:
            return self
        
        try:
            value = self._map[instance]
        except KeyError:
            value = self._method(instance)
            self._map[instance] = value

        return value

class throttle:
    def __init__(self, rate):
        self.rate = rate
        self._map = WeakKeyDictionary()

    def __call__(self, fn):
        last_time = None
        def wrapped(*args, **kwargs):
            nonlocal last_time
            this_time = time.monotonic()

            if last_time is None:
                last_time = this_time
                return fn(*args, **kwargs)
            
            delta = this_time - last_time
            if delta < self.rate:
                return

            last_time = this_time
            return fn(*args, **kwargs)
            
        return wrapped
