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
