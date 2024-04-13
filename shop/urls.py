from django.urls import path , include
from .views import *

urlpatterns = [
    path('' , index , name='index'),
    path('manage_products/' , SellerAction.manage_product , name='manage_products'),
    path('create_product/' , SellerAction.create_product , name='create_product'),
    path('edit_product/<int:id>/' , SellerAction.edit_product , name='edit_product'),
    path('view_product/<int:id>/' , SellerAction.view_product , name='view_product'),
    path('delete_product/<int:id>/' , SellerAction.delete_product , name='delete_product'),
    path('add_category/' , SellerAction.add_category , name='add_category'),
    
    # cart 
    path('add_to_cart/<int:id>/' , CartAction.add_to_cart , name='add_to_cart'),
    path('update_cart/<int:id>/' , CartAction.update_quantity , name='update_cart'),
    path('remove_from_cart/<int:id>/' , CartAction.remove_from_cart , name='remove_from_cart'),
    path('cart/' , CartAction.cart , name='cart'),
    path('checkout/' , CartAction.checkout , name='checkout'),
    path('search/', search_products, name='search_products'),
    path('orders/', orders, name='order_history'),
    path('order/<int:id>/', CartAction.order_detail, name='order_details'),

    # dashboard
    path('dashboard/' , dashboard , name='dashboard'),
]
