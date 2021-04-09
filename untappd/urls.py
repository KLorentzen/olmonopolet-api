from django.urls import path, include
from .views import sync_untappd_user, UntappdList, UntappdDetail, MappingList

urlpatterns = [
    path('sync/', sync_untappd_user, name="sync_untappd_user"),
    path('',UntappdList.as_view()),
    path('<int:beer_id>/',UntappdDetail.as_view()),
    path('mapping/',MappingList.as_view()),
]
