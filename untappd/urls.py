from django.urls import path, include
from .views import RatingList, MappingList

urlpatterns = [
    path('rating',RatingList.as_view()),
    path('mapping',MappingList.as_view()),
]
