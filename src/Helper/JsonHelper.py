import json
from os import error



class CustomJsonEncoder(json.JSONEncoder):
        def default(self, o):
            return o.__dict__   

def GetValue(JsonData, FieldName, DefaultValue):
    Response = DefaultValue

    for Item in JsonData:
        if FieldName.lower() in Item.lower():
            Response = JsonData[Item]
            break
    return Response

def HasValue(JsonData, FieldName):
    Response = False

    for Item in JsonData:
        if FieldName.lower() in Item.lower():
            Response = True
            break
    return Response


def ConvertObjectJsonString(InputObject):
    Response = ""
    try:
       Response  = json.dumps(InputObject, indent=0, cls=CustomJsonEncoder)
    except error:
        print(error)

    return Response