from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Category, Product, Cart, CartItems, Review, Wishlist

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'profile_pic_url']

class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = "__all__"
        read_only_fields = ['slug']

class ProductListSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only = True)
    class Meta:
        model = Product
        exclude = ['description']
        read_only_fields = ['slug']

class ProductDetailSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only = True)
    class Meta:
        model = Product
        fields = '__all__'
        read_only_fields = ['slug']

class CartItemSerializer(serializers.ModelSerializer):
    product = ProductListSerializer(read_only = True)
    sub_total = serializers.SerializerMethodField()
    class Meta:
        model = CartItems
        fields = ['id', 'product', 'quantity', 'sub_total']

    def get_sub_total(self, cartitem):
        total = cartitem.product.price * cartitem.quantity
        return total
    
class CartSerializer(serializers.ModelSerializer):
    cartitems = CartItemSerializer(read_only=True, many=True)
    cart_total = serializers.SerializerMethodField()
    total_quantity = serializers.SerializerMethodField()
    class Meta: 
        model = Cart
        fields = ['id', 'cart_code', 'cartitems', 'total_quantity', 'cart_total']

    def get_cart_total(self, cart):
        items = cart.cartitems.all()
        total = sum([item.quantity * item.product.price for item in items])
        return total
    
    def get_total_quantity(self, cart):
        items = cart.cartitems.all()
        total_qty = sum([item.quantity for item in items])
        return total_qty
    

class ReviewSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    class Meta:
        model = Review
        fields = ['id', 'user', 'rating', 'review', 'created', 'updated']

class WishlistSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    product = ProductListSerializer(read_only=True)
    class Meta:
        model = Wishlist
        fields = ['id','user','product','created']