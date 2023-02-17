
CREATE NONCLUSTERED INDEX IX_Users_UserID ON dbo.Users(UserID)
CREATE NONCLUSTERED INDEX IX_HotelReviews_ReviewID ON  dbo.HotelReviews(ReviewID) INCLUDE(Hotel_ID, Service)





DECLARE @Cols NVARCHAR(MAX) = (SELECT STRING_AGG('[Item_' + CAST(ID AS NVARCHAR(MAX)), '],')  FROM dbo.Hotels)

DECLARE @Query NVARCHAR(MAX) = 
' SELECT User_ID, ' + @Cols + ' FROM (
    SELECT u.ID User_ID, hr.Service Rate, hr.Hotel_ID Item_ID FROM dbo.HotelReviews hr
		JOIN dbo.Users u ON u.UserID = hr.ReviewID
) x
pivot 
(
    MAX(Rate)
    FOR Item_ID IN (' + @Cols + ')
) p '
PRINT(@Query)
execute(@Query)


SELECT User_ID, [1], [2], [3] FROM 
(
	SELECT u.ID User_ID, hr.Service Rate, hr.Hotel_ID Item_ID FROM dbo.HotelReviews hr
		JOIN dbo.Users u ON u.UserID = hr.ReviewID
	WHERE hr.Hotel_ID IN (1,2,3)
) main
PIVOT
(
	MAX(Rate)
	FOR Item_ID IN ([1], [2], [3])
) p








SELECT r.ID User_ID, ISNULL(r.Hotel_ID, h.ID) Item_ID, r.Service Rate 
FROM dbo.Hotels h
LEFT JOIN (
	SELECT u.ID, hr.Hotel_ID, hr.Service FROM dbo.HotelReviews hr
		JOIN dbo.Users u ON u.UserID = hr.ReviewID
	WHERE u.ID = 1
) r ON r.ID = h.ID

