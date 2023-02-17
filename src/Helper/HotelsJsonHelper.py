from . import JsonHelper
import Models.ObjHotels as ObjHotels
import Models.ObjHotelReviews as ObjHotelReviews

def GetHotel(JsonData) -> ObjHotels.ObjHotels:
    Hotel = ObjHotels.ObjHotels()
    Hotel.HotelID = JsonHelper.GetValue(JsonData["HotelInfo"], "HotelID", "")
    Hotel.Name = JsonHelper.GetValue(JsonData["HotelInfo"], "Name", "")
    Hotel.ImgURL = JsonHelper.GetValue(JsonData["HotelInfo"], "ImgURL", "")
    Hotel.Price = JsonHelper.GetValue(JsonData["HotelInfo"], "Price", "")
    Hotel.Address = JsonHelper.GetValue(JsonData["HotelInfo"], "Address", "")
    Hotel.HotelURL = JsonHelper.GetValue(JsonData["HotelInfo"], "HotelURL", "")
    return Hotel
def GetReviews(JsonData) -> list:
    Reviews = []
    for Item in JsonData["Reviews"]:
        Review = ObjHotelReviews.ObjHotelReviews()
        Review.AuthorLocation = JsonHelper.GetValue(Item, "AuthorLocation", "")
        Review.Title = JsonHelper.GetValue(Item, "Title", "")
        Review.Author = JsonHelper.GetValue(Item, "Author", "")
        Review.ReviewID = JsonHelper.GetValue(Item, "ReviewID", "")
        Review.Content = JsonHelper.GetValue(Item, "Content", "")
        Review.Date = JsonHelper.GetValue(Item, "Date", "")

        if JsonHelper.HasValue(Item["Ratings"], "service"):
            Review.Service = int(float(JsonHelper.GetValue(Item["Ratings"], "service", 0)))        

        if JsonHelper.HasValue(Item["Ratings"], "cleanliness"):
            Review.Cleanliness = int(float(JsonHelper.GetValue(Item["Ratings"], "cleanliness", 0)))

        if JsonHelper.HasValue(Item["Ratings"], "overall"):
            Review.Overall = int(float(JsonHelper.GetValue(Item["Ratings"], "overall", 0)))

        if JsonHelper.HasValue(Item["Ratings"], "value"):
            Review.Value = int(float(JsonHelper.GetValue(Item["Ratings"], "value", 0)))

        if JsonHelper.HasValue(Item["Ratings"], "sleep quality"):
            Review.SleepQuality = int(float(JsonHelper.GetValue(Item["Ratings"], "sleep quality", 0)))

        if JsonHelper.HasValue(Item["Ratings"], "location"):
            Review.Location = int(float(JsonHelper.GetValue(Item["Ratings"], "location", 0)))

        if JsonHelper.HasValue(Item["Ratings"], "rooms"):
            Review.Rooms = int(float(JsonHelper.GetValue(Item["Ratings"], "rooms", 0)))

        if JsonHelper.HasValue(Item["Ratings"], "business service"):
            Review.BusinessService = int(float(JsonHelper.GetValue(Item["Ratings"], "business service", 0)))

        if JsonHelper.HasValue(Item["Ratings"], "Check in / front desk"):
            Review.CheckInFrontDesk = int(float(JsonHelper.GetValue(Item["Ratings"], "Check in / front desk", 0)))
        
        
        Reviews.append(Review)
    
    return Reviews

