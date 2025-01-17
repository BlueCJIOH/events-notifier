from config.base import BaseEnum


class MembershipStatusEnum(BaseEnum):
    ACTIVE = "active"
    INACTIVE = "inactive"

    @classmethod
    def is_valid_status(cls, status):
        return status in cls._value2member_map_
