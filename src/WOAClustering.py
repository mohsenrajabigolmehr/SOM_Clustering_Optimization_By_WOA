from os import error
import numpy as np
import pandas as pd
from sklearn.metrics import silhouette_score
from sklearn.metrics import davies_bouldin_score
from sklearn.metrics import calinski_harabasz_score

from WOA.WhaleBatchClustring import WhaleBatchClustring


from Models.Core.ObjGlobalRequest import ObjGlobalRequest
import Models.ObjHotelReviews as ObjHotelReviews

import Repository.HotelReviewsRepository as HotelReviewsRepository
import Repository.UsersRepository as UsersRepository

import Helper.ListHelper as ListHelper

Users = UsersRepository.GetList(ObjGlobalRequest())

User = ObjHotelReviews.ObjHotelReviews_GetList_Request()
User.User_ID = Users.List[0]["User_ID"]
ReviewsRequest0 = ObjGlobalRequest(User)
ReviewsResponse0 = HotelReviewsRepository.GetList(ReviewsRequest0)


Matrix = []
MatrixSize = len(ReviewsResponse0.List)
BatchSize = 1000
Clusters = 13

_silhouette_score = 0
_bouldin_score = 0
_calinski_harabasz_score = 0

Whale = WhaleBatchClustring(2, Clusters, BatchSize)
BatchNumber = 0
index = 0
indexData = 0
for u in Users.List:
    
    if(index == 0):
        Matrix = np.zeros((BatchSize,MatrixSize), dtype=int)   

    User = ObjHotelReviews.ObjHotelReviews_GetList_Request()
    User.User_ID = u["User_ID"]    
    ReviewsRequest = ObjGlobalRequest(User)
    ReviewsResponse = HotelReviewsRepository.GetList(ReviewsRequest)
    UsersReviews_DataFrame = pd.DataFrame(ReviewsResponse.List)
    Matrix[index] = UsersReviews_DataFrame["Rate"]
    
    print(f"indexData: {indexData}, User_ID: {u['User_ID']}" , end="\r")

    index += 1
    indexData += 1
    if (index + 1 == BatchSize):
        
        BatchNumber += 1
        print("\n Batch Number : ", BatchNumber)

        Whale = Whale.PartialFit(Matrix)

        Unique_Labels = ListHelper.Unique(Whale.Labels[Whale.BestSolutionIndex])
        if (len(Unique_Labels) == 1):
            if(Whale.Labels[Whale.BestSolutionIndex][0] == 0):
                Whale.Labels[Whale.BestSolutionIndex][0] = 1
            else:
                Whale.Labels[Whale.BestSolutionIndex][0] = 0

        _silhouette_score += silhouette_score(Matrix, Whale.Labels[Whale.BestSolutionIndex], metric="euclidean")
        _bouldin_score += davies_bouldin_score(Matrix, Whale.Labels[Whale.BestSolutionIndex])
        _calinski_harabasz_score += calinski_harabasz_score(Matrix, Whale.Labels[Whale.BestSolutionIndex])
        index = 0


print("For n_clusters =", Clusters, "The silhouette_score is :", _silhouette_score)
print("For n_clusters =", Clusters, "The bouldin_score is :", _bouldin_score, "lower Is better")
print("For n_clusters =", Clusters, "The calinski_harabasz_score is :", _calinski_harabasz_score, "higher Is better")


print("End Of WOA Clustering")
