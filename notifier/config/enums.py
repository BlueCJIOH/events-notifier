from enum import Enum

class BaseEnum(Enum):
    @classmethod
    def choices(cls):
        return [(status.value, status.name.title()) for status in cls]
