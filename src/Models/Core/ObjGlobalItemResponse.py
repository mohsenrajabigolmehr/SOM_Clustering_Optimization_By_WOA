from enum import Enum
from typing import Any
from Models.Core.Enums import StatusCode

class ObjGlobalItemResponse:
    def __init__(self, IsSuccess: bool, StatusCode: StatusCode, Message: str, Item: Any):
        self.IsSuccess = IsSuccess
        self.StatusCode = StatusCode
        self.Message = Message
        self.Item = Item
    def __str__(self) -> str:
        return str("StatusCode: " + str(self.StatusCode) + ", IsSuccess: " + str(self.IsSuccess))
    def Map(self, Source):
        self.StatusCode = Source.StatusCode
        self.IsSuccess = Source.IsSuccess
        self.Message = Source.Message
