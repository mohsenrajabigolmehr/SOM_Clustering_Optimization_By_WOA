from Models.Core.ObjGlobalRequest import ObjGlobalRequest
from Models.Core.ObjGlobalItemResponse import ObjGlobalItemResponse
from Models.Core.ObjGlobalListResponse import ObjGlobalListResponse
import SQLDataAccessLayer.UsersSQLDataAccessLayer as UsersSQLDataAccessLayer
 

def GetList(Request: ObjGlobalRequest) -> ObjGlobalListResponse:
    Response = UsersSQLDataAccessLayer.GetList(Request)
    return  Response
