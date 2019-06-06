
from enum import IntEnum as Enum


class BasePremiumException(Exception):
    pass


class ConstError(BasePremiumException):
    pass


class IntEnum(Enum):
    @staticmethod
    def find_enum(cls, value):
        for k, v in cls._value2member_map_.items():
            if k == value:
                return v
        return None


class ErrorCode(IntEnum):
    """ 错误码 """

    not_found = 404
    bad_request = 400
    unauthorized = 401
    forbidden = 403
    not_allowed = 405
    not_acceptable = 406
    conflict = 409
    gone = 410
    precondition_failed = 412
    request_entity_too_large = 413
    unsupport_media_type = 415
    internal_server_error = 500
    service_unavailable = 503
    service_not_implemented = 501
    handler_uncatched_exception = 504
    config_import_error = 1001
    config_item_notfound_error = 1002