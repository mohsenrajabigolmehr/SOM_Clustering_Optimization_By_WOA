import numpy as np
import pandas as pd 
from sklearn.cluster import MiniBatchKMeans
from sklearn.metrics import silhouette_score
from sklearn.metrics import davies_bouldin_score
from sklearn.metrics import calinski_harabasz_score

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

kmeans_3 = MiniBatchKMeans(n_clusters=3, random_state=1, batch_size=BatchSize, verbose=0)
kmeans_5 = MiniBatchKMeans(n_clusters=5, random_state=1, batch_size=BatchSize, verbose=0)
kmeans_7 = MiniBatchKMeans(n_clusters=7, random_state=1, batch_size=BatchSize, verbose=0)
kmeans_9 = MiniBatchKMeans(n_clusters=9, random_state=1, batch_size=BatchSize, verbose=0)
kmeans_11 = MiniBatchKMeans(n_clusters=11, random_state=1, batch_size=BatchSize, verbose=0)
kmeans_13 = MiniBatchKMeans(n_clusters=13, random_state=1, batch_size=BatchSize, verbose=0)
kmeans_15 = MiniBatchKMeans(n_clusters=15, random_state=1, batch_size=BatchSize, verbose=0)

score_3 = { 'silhouette': 0, 'bouldin': 0, 'calinski_harabasz': 0 }
score_5 = { 'silhouette': 0, 'bouldin': 0, 'calinski_harabasz': 0 }
score_7 = { 'silhouette': 0, 'bouldin': 0, 'calinski_harabasz': 0 }
score_9 = { 'silhouette': 0, 'bouldin': 0, 'calinski_harabasz': 0 }
score_11 = { 'silhouette': 0, 'bouldin': 0, 'calinski_harabasz': 0 }
score_13 = { 'silhouette': 0, 'bouldin': 0, 'calinski_harabasz': 0 }
score_15 = { 'silhouette': 0, 'bouldin': 0, 'calinski_harabasz': 0 }

def fn_train(Matrix, kmeans, score):
    kmeans = kmeans.partial_fit(Matrix)
    kmeans.fit_predict(Matrix)
    Unique_Labels = ListHelper.Unique(kmeans.labels_)
    if (len(Unique_Labels) > 1):
        score['silhouette'] += silhouette_score(Matrix, kmeans.labels_, metric="euclidean")
        score['bouldin'] += davies_bouldin_score(Matrix, kmeans.labels_)
        score['calinski_harabasz'] += calinski_harabasz_score(Matrix, kmeans.labels_)
    else :
        print("Warning single cluster")
        score['silhouette'] += 0
        score['bouldin'] += 0
        score['calinski_harabasz'] += 0
    return score

BatchNumber = 0
index = 0
for u in Users.List:
    
    if(index == 0):
        Matrix = np.zeros((BatchSize,MatrixSize), dtype=int)   

    User = ObjHotelReviews.ObjHotelReviews_GetList_Request()
    User.User_ID = u["User_ID"]    
    ReviewsRequest = ObjGlobalRequest(User)
    ReviewsResponse = HotelReviewsRepository.GetList(ReviewsRequest)
    UsersReviews_DataFrame = pd.DataFrame(ReviewsResponse.List)
    Matrix[index] = UsersReviews_DataFrame["Rate"]
    
    
    index += 1
    if (index + 1 == BatchSize):
        BatchNumber += 1
        print("Batch Number : ", BatchNumber)

        score_3 = fn_train(Matrix, kmeans_3, score_3)
        score_5 = fn_train(Matrix, kmeans_5, score_5)
        score_7 = fn_train(Matrix, kmeans_7, score_7)
        score_9 = fn_train(Matrix, kmeans_9, score_9)
        score_11 = fn_train(Matrix, kmeans_11, score_11)
        score_13 = fn_train(Matrix, kmeans_13, score_13)
        score_15 = fn_train(Matrix, kmeans_15, score_15)
        
        index = 0
    

print("For n_clusters = 3 The score is :", score_3)
print("For n_clusters = 5 The score is :", score_5)
print("For n_clusters = 7 The score is :", score_7)
print("For n_clusters = 9 The score is :", score_9)
print("For n_clusters = 11 The score is :", score_11)
print("For n_clusters = 13 The score is :", score_13)
print("For n_clusters = 15 The score is :", score_15)



print("End Of Kmeans Clustering")

# For n_clusters = 3 The score is : {'silhouette': 2.9841307038329186, 'bouldin': 49.86372885677584, 'calinski_harabasz': 500.4161077803982}
# For n_clusters = 5 The score is : {'silhouette': 2.277131312672374, 'bouldin': 49.72536545386402, 'calinski_harabasz': 522.704438024472}
# For n_clusters = 7 The score is : {'silhouette': 2.1626997855412906, 'bouldin': 49.1082434168499, 'calinski_harabasz': 488.16167626292867}
# For n_clusters = 9 The score is : {'silhouette': 2.025614861073706, 'bouldin': 49.2220856274955, 'calinski_harabasz': 535.0935592843236}
# For n_clusters = 11 The score is : {'silhouette': 2.5747930744100387, 'bouldin': 48.3062643304115, 'calinski_harabasz': 526.9421185898276}
# For n_clusters = 13 The score is : {'silhouette': 2.3353341421605354, 'bouldin': 48.279202096976924, 'calinski_harabasz': 532.2379804336362}
# For n_clusters = 15 The score is : {'silhouette': 3.2168037034775003, 'bouldin': 48.01903921991596, 'calinski_harabasz': 524.0385937748065}



# For n_clusters = 3 The score is : {'silhouette': 0.4633232232035958, 'bouldin': 10.368552507398116, 'calinski_harabasz': 100.8524777498789}
# For n_clusters = 5 The score is : {'silhouette': 0.3623201204006951, 'bouldin': 10.238619542616288, 'calinski_harabasz': 95.53560310211674}
# For n_clusters = 7 The score is : {'silhouette': 0.032488188544795904, 'bouldin': 10.089111177943835, 'calinski_harabasz': 83.96569089064928}
# For n_clusters = 9 The score is : {'silhouette': 0.49734703612564557, 'bouldin': 9.67816653501789, 'calinski_harabasz': 104.02872784421956}
# For n_clusters = 11 The score is : {'silhouette': -0.006564890849287082, 'bouldin': 10.411274770398451, 'calinski_harabasz': 102.42499822036115}
# For n_clusters = 13 The score is : {'silhouette': 0.5565909506869793, 'bouldin': 9.685668329143853, 'calinski_harabasz': 107.17019482278161}
# For n_clusters = 15 The score is : {'silhouette': 0.43359315227750567, 'bouldin': 10.001975023774738, 'calinski_harabasz': 97.98500282350041}

