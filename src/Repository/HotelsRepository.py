from Models.Core.ObjGlobalRequest import ObjGlobalRequest
from Models.Core.ObjGlobalItemResponse import ObjGlobalItemResponse
from Models.Core.ObjGlobalListResponse import ObjGlobalListResponse
import SQLDataAccessLayer.HotelsSQLDataAccessLayer as HotelsSQLDataAccessLayer
 

def Add(Request: ObjGlobalRequest) -> ObjGlobalItemResponse:
    Response = HotelsSQLDataAccessLayer.Add(Request)
    return  Response

def GetList(Request: ObjGlobalRequest) -> ObjGlobalListResponse:
    Response = HotelsSQLDataAccessLayer.GetList(Request)
    return  Response
