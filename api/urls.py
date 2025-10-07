from django.urls import path
from . import views

urlpatterns = [
    # path('products/', views.product_list, name='product-list'),
    path('products/', views.ProductListAPIView.as_view(), name='product-list'),
    # path("products/<int:pk>/", views.product_detail, name="product-detail"),
    path("products/<int:pk>/", views.ProductDetailAPIView.as_view(), name="product-detail"),
    # path("orders/", views.order_list, name="order-list"),
    path("orders/", views.OrderListAPIView.as_view(), name="order-list"),
    # path("products/info/", views.product_detail, name="product-detail-info"),
    path("products/info/", views.ProductDetailInfoAPIView.as_view(), name="product-detail-info"),
    
    path("user-orders/", views.UserOrderListAPIView.as_view(), name="user-order-list"),
]
