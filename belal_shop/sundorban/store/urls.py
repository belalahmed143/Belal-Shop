from django.urls import path
from .views import *



urlpatterns =[
    path('',ProductView.as_view(), name='home'),
    path('product/detail/<slug>/', ProductDetail.as_view(), name='product-detail'),
    path('products/category/<name>/', ProductCategoryFiltering.as_view(), name='category'),
    path('ProductSearch/',ProductSearchView.as_view(), name = 'search'),
    path('add-to-cart/<slug>/', add_to_cart, name='add-to-cart'),
    path("wish_list/", wish_list, name="wish-list"),
    path('add_to_wishlist/<slug>', add_to_wishlist, name='add-to-wishlist'),
    path('delete_wish_list/<slug>', delete_wish_list, name='delete-wish-list'),
    path('add-coupon/', AddCouponView.as_view(), name='add-coupon'),
    path("cart_summary", CartSummary.as_view(), name="cart-summary"),
    path("PrductQuantityIncrement/<slug>", PrductQuantityIncrement.as_view(), name="Prduct-Quantity-Increment"),
    path("PrductQuantityDecrementr/<slug>", PrductQuantityDecrementr.as_view(), name="Prduct-Quantity-Decrementr"),
]
