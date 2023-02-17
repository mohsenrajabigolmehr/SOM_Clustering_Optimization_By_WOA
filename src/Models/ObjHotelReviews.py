class ObjHotelReviews:
    def __init__(self):
        self.ID = 0
        self.Hotel_ID = 0
        self.AuthorLocation = ""
        self.Title = ""
        self.Author = ""
        self.ReviewID = ""
        self.Content = ""
        self.Date = ""
        self.Service = None
        self.Cleanliness = None
        self.Overall = None
        self.Value = None
        self.SleepQuality = None
        self.Location = None
        self.Rooms = None
        self.BusinessService = None
        self.CheckInFrontDesk = None
    def __str__(self) -> str:
        return str("ID: " + str(self.ID) + ", Hotel_ID: " + str(self.Hotel_ID) + ", ReviewID: " + str(self.ReviewID))


class ObjHotelReviews_GetList_Response:
    def __init__(self):
        self.Item_ID = 0
        self.Rate = 0
       

class ObjHotelReviews_GetList_Request:
    def __init__(self):
        self.User_ID = 0
