import json
import os
import Helper.JsonHelper as JsonHelper
import Helper.HotelsJsonHelper as HotelsJsonHelper
from Models.ObjHotelReviews import ObjHotelReviews
from Models.ObjHotelReviewsForBatchInsert import ObjHotelReviewsForBatchInsert
import Repository.HotelsRepository as HotelsRepository
import Repository.HotelReviewsRepository as HotelReviewsRepository
from Models.Core.ObjGlobalRequest import ObjGlobalRequest
 

Path = "datasets/TripAdvisorJson/json/"
Entries = os.listdir(Path)
Index = 0
for Entry in Entries:

    JsonFile = open(Path + Entry, "r")
    JsonData = json.loads(JsonFile.read())
    Hotel = HotelsJsonHelper.GetHotel(JsonData)

    RequestHotelAdd = ObjGlobalRequest(Hotel)
    ResponseHotelAdd = HotelsRepository.Add(RequestHotelAdd)
    #print(ResponseHotelAdd.Item)

    if ResponseHotelAdd.IsSuccess == False:
        continue

    Reviews = HotelsJsonHelper.GetReviews(JsonData)
    for Review in Reviews:
        Review.Hotel_ID = ResponseHotelAdd.Item.ID
        
    ReviewsForBatchInsert = ObjHotelReviewsForBatchInsert(JsonHelper.ConvertObjectJsonString(Reviews))
    RequestHotelReviewAdd = ObjGlobalRequest(ReviewsForBatchInsert)
    ResponseHotelReviewAdd = HotelReviewsRepository.Add(RequestHotelReviewAdd)
    #print(ResponseHotelReviewAdd)
    
    
    Index += 1
    print(str(Index))
    #if Index > 1500:
        #break
    

print("End Of DataPreProcessing")