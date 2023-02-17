class ObjUsers:

    def __init__(self):
        self.ID = 0
        self.UserID = ""        
    def __str__(self) -> str:
        return str("ID: " + str(self.ID) + ", UserID: " + self.UserID)