import json
import os.path

def GetConnectionString(Name):
    ConnectionString = ""
    
    ConfigFile = open(os.path.dirname(__file__) + "/../SystemConfig.Json", "r")
    ConfigJson = json.loads(ConfigFile.read())
    
    ConnectionString = ConfigJson["SQLServerConnectionStrings"][Name]

    return ConnectionString

