from Models.Core.ObjGlobalRequest import ObjGlobalRequest
from Models.Core.ObjGlobalItemResponse import ObjGlobalItemResponse
from Models.Core.ObjGlobalListResponse import ObjGlobalListResponse
import SQLDataAccessLayer.HotelReviewsSQLDataAccessLayer as HotelReviewsSQLDataAccessLayer
 

def Add(Request: ObjGlobalRequest) -> ObjGlobalItemResponse:
    Response = HotelReviewsSQLDataAccessLayer.Add(Request)
    return  Response

def GetList(Request: ObjGlobalRequest) -> ObjGlobalListResponse:
    Response = HotelReviewsSQLDataAccessLayer.GetList(Request)
    return  Response
