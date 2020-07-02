from django.urls import path, include
from .views import RatingList, RatingDetail, MappingList

urlpatterns = [
    path('rating',RatingList.as_view()),
    path('rating/<int:beer_id>',RatingDetail.as_view()),
    path('mapping',MappingList.as_view()),
]
