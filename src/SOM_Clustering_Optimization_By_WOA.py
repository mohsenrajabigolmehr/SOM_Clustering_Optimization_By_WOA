from os import error
import numpy as np
import pandas as pd
from numpy.core.fromnumeric import shape
from sklearn.metrics import silhouette_score
from sklearn.metrics import davies_bouldin_score
from sklearn.metrics import calinski_harabasz_score

from SOM.SelfOrganisingMaps import SelfOrganisingMaps

from WOA.WhaleClustersOptimization import WhaleClustersOptimization

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

# ماتریس کاربر هتل
Matrix = []
MatrixSize = len(ReviewsResponse0.List)
BatchSize = 1000
Clusters = 13

# ساخت شی SOM با توجه به تعداد خوشه و ماتریس کاربر-هتل
SOM = SelfOrganisingMaps(Clusters, MatrixSize, 50)

_silhouette_score = 0
_bouldin_score = 0
_calinski_harabasz_score = 0

BatchNumber = 0
index = 0
indexData = 0

# حلقه برای هر 10000 کاربر
for u in Users.List:

    # انتصاب سایز ماتریس کاربر هتل 
    if(index == 0):
        Matrix = np.zeros((BatchSize, MatrixSize), dtype=int)

    # به ازای هر کاربر تمام نظرات کاربر برای هتل ها جمع اوری میشود
    # و در ماتریس کاربر-هتل قرارداده میشود
    User = ObjHotelReviews.ObjHotelReviews_GetList_Request()
    User.User_ID = u["User_ID"]
    ReviewsRequest = ObjGlobalRequest(User)
    ReviewsResponse = HotelReviewsRepository.GetList(ReviewsRequest)
    UsersReviews_DataFrame = pd.DataFrame(ReviewsResponse.List)
    Matrix[index] = UsersReviews_DataFrame["Rate"]

    print(f"indexData: {indexData}, User_ID: {u['User_ID']}" , end="\r")

    # اگر سایز مناسب دسته شده باشد این دسته 1000 تایی آموزش داده میشود
    index += 1
    indexData += 1
    if (index + 1 == BatchSize):

        BatchNumber += 1
        print("\n Batch Number: ", BatchNumber)
        # خوشه بندی با SOM
        SOM.Fit(Matrix)
        
        # print("shape Matrix: ", shape(Matrix))
        
        # Optimization Cluster Centers  
        print(shape(SOM.Weights))

        # ساخت شی WOA برای بهینه سازی  مرکز خوشه ها که همان وزن یال های  SOM هستند
        woa = WhaleClustersOptimization(SOM.Weights, SOM.Labels, Matrix)
        # print(shape(woa.basePoint))        
        # print(shape(woa._sols))
        
        # اجرای WOA به تعداد 10 بار
        for _ in range(10):
            woa.optimize()
        
        # print(shape(woa._best_solution))
        # print(woa._best_solution)
        
        # انصاب بهترین نتیجه WOA به عنوان وزن یال های SOM یا همان مرکز خوشه ها
        SOM.Weights = woa._best_solution

        Unique_Labels = ListHelper.Unique(SOM.Labels)
        if (len(Unique_Labels) == 1):
            if(SOM.Labels[0] == 0):
                SOM.Labels[0] = 1
            else:
                SOM.Labels[0] = 0

        # محاسبه معیار ها به صورت بدون ناظر و با معیار فاصله اقلیدوسی
        _silhouette_score += silhouette_score(Matrix, SOM.Labels, metric="euclidean")
        _bouldin_score += davies_bouldin_score(Matrix, SOM.Labels)
        _calinski_harabasz_score += calinski_harabasz_score(Matrix, SOM.Labels)
        
        index = 0


# نمایش نتایج اعتبار سنجی ها
print("For n_clusters =", Clusters, "The silhouette_score is :", _silhouette_score)
print("For n_clusters =", Clusters, "The bouldin_score is :", _bouldin_score, "lower Is better")
print("For n_clusters =", Clusters, "The calinski_harabasz_score is :", _calinski_harabasz_score, "higher Is better")

print("End Of SOM Clustering")


# For n_clusters = 3 The silhouette_score is : 0
# For n_clusters = 3 The bouldin_score is : 0 lower Is better
# For n_clusters = 3 The calinski_harabasz_score is : 0 higher Is better





