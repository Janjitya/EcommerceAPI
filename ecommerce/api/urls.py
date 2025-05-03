from django.urls import path,include
from . import views


urlpatterns = [
    
    path('product_list/', views.ProductListView.as_view(), name="product_list"),
    path('products/', views.SearchProduct.as_view(), name="search_products"),
    path('products/<slug:slug>', views.ProductDetailView.as_view(), name="product_detail"),
    path('category_list/', views.CategoryListView.as_view(), name="category_list"),
    path('category/<slug:slug>', views.CategoryDetailView.as_view(), name="category_detail"),
    path('add_to_cart/', views.AddToCart.as_view(), name="add_to_cart"),
    path('update_quantity/', views.UpdateItemQty.as_view(), name="update_quantity"),
    path('delete_cart_item/<int:pk>', views.DeleteCartItem.as_view(), name='delete_cart_item'),
    path('add_review/', views.AddReview.as_view(), name="add_review"),
    path("review/<int:pk>/",views.UpdateOrDeleteReview.as_view(), name="update_delete_update"),
    path('add_to_wishlist/', views.AddToWishlist.as_view(), name="add_to_wishlist"),
]
