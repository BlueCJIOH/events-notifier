from enum import Enum, unique
from functools import lru_cache
from operator import attrgetter
from functools import wraps


@unique
class BaseEnum(Enum):
    @classmethod
    @lru_cache(None)
    def values(cls):
        return tuple(map(attrgetter("value"), cls))

    @classmethod
    @lru_cache(None)
    def names(cls):
        return tuple(map(attrgetter("name"), cls))

    @classmethod
    @lru_cache(None)
    def items(cls):
        return tuple(zip(cls.values(), cls.names()))

    @classmethod
    @lru_cache(None)
    def revert_items(cls):
        return tuple(zip(cls.names(), cls.values()))

    @classmethod
    @lru_cache(None)
    def members(cls):
        return dict(cls.items())

    @classmethod
    @lru_cache(None)
    def revert_members(cls):
        return dict(cls.revert_items())

    @classmethod
    @lru_cache(None)
    def exclude_values(cls, *items):
        return tuple(set((map(attrgetter("value"), cls))) - set(items))


NULLABLE = {
    "null": True,
    "blank": True,
}


def require_permission(permission_name):
    def decorator(view_method):
        @wraps(view_method)
        def _wrapped_view(*args, **kwargs):
            return view_method(*args, **kwargs)

        setattr(_wrapped_view, "required_permission", permission_name)
        return _wrapped_view

    return decorator
