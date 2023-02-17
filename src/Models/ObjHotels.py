class ObjHotels:

    def __init__(self):
        self.ID = 0
        self.Name = ""
        self.HotelURL = ""
        self.Price = ""
        self.Address = ""
        self.HotelID = ""
        self.ImgURL = ""
    def __str__(self) -> str:
        return str("ID: " + str(self.ID) + ", HotelID: " + self.HotelID)
