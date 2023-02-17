class ObjGlobalListResponse:

    def __init__(self, IsSuccess: bool, StatusCode: int, Message: str, List: list):
        self.IsSuccess = IsSuccess
        self.StatusCode = StatusCode
        self.Message = Message
        self.List = List
    def __str__(self) -> str:
        return str("StatusCode: " + str(self.StatusCode) + ", IsSuccess: " + str(self.IsSuccess))
    def Map(self, Source):
        self.StatusCode = Source.StatusCode
        self.IsSuccess = Source.IsSuccess
        self.Message = Source.Message        
