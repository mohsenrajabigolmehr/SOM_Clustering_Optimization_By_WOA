from enum import Enum
from os import error
import Helper.DictHelper as DictHelper
from Models.Core.ObjGlobalItemResponse import ObjGlobalItemResponse
from Models.Core.ObjGlobalListResponse import ObjGlobalListResponse
from Models.Core.ObjGlobalRequest import ObjGlobalRequest
import Helper.SqlHelper as SqlHelper
from Models.Core.Enums import StatusCode

__DBPREFIX = "dbo.RPC_HotelReviews_"
__CONNECTION_NAME = "Hotel_Recommender_By_WOA"

def Add(Request: ObjGlobalRequest) -> ObjGlobalItemResponse:

    Response = ObjGlobalItemResponse(False, StatusCode.UNKNOWN, "", None)
    
    try:
        RequestDB =  DictHelper.ConvertFromClass(Request.Item, ["ID"])        
        ResponseDB = SqlHelper.ExecuteRpcForItem(__CONNECTION_NAME, __DBPREFIX + "Insert", RequestDB)
        Response.Map(ResponseDB)

    except error:
        print(error)

    return Response


def GetList(Request: ObjGlobalRequest) -> ObjGlobalListResponse:

    Response = ObjGlobalItemResponse(False, StatusCode.UNKNOWN, "", None)
    
    try:
        RequestDB = DictHelper.ConvertFromClass(Request.Item)
        ResponseDB = SqlHelper.ExecuteRpcForList(__CONNECTION_NAME, __DBPREFIX + "GetList", RequestDB)
        Response.Map(ResponseDB)
        if Response.IsSuccess :    
            Response.List = ResponseDB.List

    except error:
        print(error)

    return Response

