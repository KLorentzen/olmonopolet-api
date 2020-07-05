from django.urls import path, include
from .views import UntappdList, UntappdDetail, MappingList

urlpatterns = [
    path('',UntappdList.as_view()),
    path('<int:beer_id>',UntappdDetail.as_view()),
    path('mapping',MappingList.as_view()),
]
