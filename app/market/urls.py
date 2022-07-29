from django.urls import path

from market import views


app_name = 'market'

urlpatterns = [
    path('product/', views.ProductAPIView.as_view(), name='product'),
    path('unit/', views.UnitAPIView.as_view(), name='unit'),
    path('address/', views.AddressAPIView.as_view(), name='address'),
    path('order/', views.OrderListAPIView.as_view(), name='order-list'),
    path('order/create/', views.OrderCreateAPIView.as_view(), name='order-create'),
    path('order/<int:pk>/', views.OrderDetailAPIView.as_view(), name='order-detail'),
    path('item/create/', views.OrderItemCreateAPIView.as_view(), name='item-create'),
    path('fullorder/create/', views.FullOrderCreateAPIView.as_view(), name='fullorder-create'),
]
