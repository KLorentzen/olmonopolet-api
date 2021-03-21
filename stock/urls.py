from django.urls import path, include
from .views import StockChangeTemplateView, stock_change_in, stock_change_out

urlpatterns = [
    path('changes/<int:store_id>/in/',stock_change_in, name='stock_change_in'),
    path('changes/<int:store_id>/out/',stock_change_out, name='stock_change_out'),
    path('changes/<int:store_id>/',StockChangeTemplateView.as_view(), name='stock_change'),
]
