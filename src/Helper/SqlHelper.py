import pyodbc
from Models.Core.Enums import StatusCode
from Models.Core.ObjGlobalItemResponse import ObjGlobalItemResponse
from Models.Core.ObjGlobalListResponse import ObjGlobalListResponse
from . import ConfigHelper

def ExecuteRpcForItem(ConnectionName: str, RpcName: str, Parameters: dict = []) -> ObjGlobalItemResponse:

    Response = ObjGlobalItemResponse(False, StatusCode.UNKNOWN, "", None)
    ConnectionString = ConfigHelper.GetConnectionString(ConnectionName)
    conn = pyodbc.connect('Driver={SQL Server};' + ConnectionString, autocommit=True)
    cursor = conn.cursor()

    try:
        IniResponse = []

        query = "SET NOCOUNT ON; EXEC " + RpcName
        ParametersValues = []
        Index = 0
        for parameter in Parameters:
            Index += 1
            if Index < len(Parameters):
                query += " @" + parameter + " = ?, "
            else:
                query += " @" + parameter + " = ? "
            ParametersValues.append(Parameters[parameter])

        #print(query)

        cursor.execute(query, ParametersValues)
        columns = [column[0] for column in cursor.description]
        
        #print(columns)
        #TODO Convert List of Any To List of objects
        for row in cursor.fetchall():
            IniResponse.append(dict(zip(columns, row)))

        Item = IniResponse[0]
        Response.StatusCode = StatusCode(int(Item["StatusCode"]))
        Response.IsSuccess = Response.StatusCode == StatusCode.OK
        Response.Message = ""
        if Response.IsSuccess == True:
            Response.Item = Item


    except pyodbc.Error as ex:
        print(ex)
    finally:
        cursor.close()
        del cursor
        conn.close()


    return Response

#TODO Create Private Method for pure rpc call
def ExecuteRpcForList(ConnectionName: str, RpcName: str, Parameters: dict = []) -> ObjGlobalListResponse:

    Response = ObjGlobalListResponse(False, StatusCode.UNKNOWN, "", None)
    ConnectionString = ConfigHelper.GetConnectionString(ConnectionName)
    conn = pyodbc.connect('Driver={SQL Server};' + ConnectionString, autocommit=True)
    cursor = conn.cursor()

    try:
        IniResponse = []

        query = "SET NOCOUNT ON; EXEC " + RpcName
        ParametersValues = []
        Index = 0
        for parameter in Parameters:
            Index += 1
            if Index < len(Parameters):
                query += " @" + parameter + " = ?, "
            else:
                query += " @" + parameter + " = ? "
            ParametersValues.append(Parameters[parameter])

        #print(query)

        cursor.execute(query, ParametersValues)

        FirstRow  = cursor.fetchone()
        
        columns = [column[0] for column in cursor.description]
        columns.remove("StatusCode")
        #print(columns)

        #TODO Convert List of Any To List of objects

        Response.StatusCode = StatusCode(int(FirstRow.StatusCode))
        Response.IsSuccess = Response.StatusCode == StatusCode.OK
        Response.Message = ""
        if Response.IsSuccess == True:
            IniResponse.append(dict(zip(columns, FirstRow[1:])))    
            for row in cursor.fetchall():
                IniResponse.append(dict(zip(columns, row[1:])))    
            Response.List = IniResponse
        
        
    except pyodbc.Error as ex:
        print(ex)
    finally:
        cursor.close()
        del cursor
        conn.close()


    return Response
