from django.urls import path
from .views import *



urlpatterns = [
    path('',home.as_view(), name="index"),
    path('product/<int:product_id>',productdetail.as_view(), name = "productdetail"),
    path('category/<str:category_name>/', CategoryView.as_view(), name='category-view'),
    path('product-list', productlist.as_view()),
    path('searchproduct',searchproduct.as_view(), name='searchproduct'),
    path('add-to-cart',addtocart.as_view(), name="addtocart"),
    path('cart',cart.as_view(), name='cart' ),
    path('update-cart', updatecart.as_view(), name='updatecart'),
    path('delete-cart-item',deletecartitem.as_view(), name='deletecartitem'),
    path('wishlist', wishlist.as_view(), name='wishlist'),
    path('add-to-wishlist',addtowishlist.as_view(), name='addtowishlist'),
    path('delete-wishlist-item', deletewishlistitem.as_view(), name='deletewishlistitem'),
    path('checkoutpage', checkoutpage.as_view(), name='checkoutpage'), 
    path('place-order', placeorder.as_view(), name='placeorder'),
    path('store', store.as_view(), name='store')

]
