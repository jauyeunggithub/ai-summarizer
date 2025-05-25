from enum import Enum


class StatusEnum(Enum):
    PROCESSING = 'processing'
    COMPLETE = 'complete'
    ERROR = 'error'
