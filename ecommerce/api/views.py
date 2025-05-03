from django.shortcuts import render, get_object_or_404
from django.contrib.auth import get_user_model
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status,filters
from django.db.models import Q
from .serializers import CategorySerializer, ProductListSerializer, ProductDetailSerializer, CartItemSerializer, CartSerializer, ReviewSerializer, WishlistSerializer
from .models import Category, Product, Cart, CartItems, Review, Wishlist

# Create your views here.
User = get_user_model()
class ProductListView(APIView):

    def get(self, request):
        prodcuts = Product.objects.filter(featured=True)
        serializer = ProductListSerializer(prodcuts, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

class SearchProduct(APIView):

    def get(self, request):
        search = request.query_params.get('search','')

        if search:
            products = Product.objects.filter(
                Q(product_name__icontains=search) |
                Q(description__icontains=search) |
                Q(category__category_name__icontains=search)    
            )
        else:
            products = Product.objects.all()

        serializer = ProductListSerializer(products, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    
class ProductDetailView(APIView):

    def get(self, request, slug):
        product = Product.objects.get(slug = slug)
        serializer = ProductDetailSerializer(product)

        return Response(serializer.data, status=status.HTTP_200_OK)
    
class CategoryListView(APIView):

    def get(self, request):
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)
    
class CategoryDetailView(APIView):

    def get(self, request, slug):
        category = get_object_or_404(Category, slug=slug)
        serializer = CategorySerializer(category)

        return Response(serializer.data, status=status.HTTP_200_OK)
    
class AddToCart(APIView):

    def post(self, request):
        cart_code = request.data.get('cart_code')
        product_id = request.data.get('product_id')

        cart, created = Cart.objects.get_or_create(cart_code=cart_code)
        product = Product.objects.get(id = product_id)

        cartitem, created = CartItems.objects.get_or_create(cart=cart, product=product)

        if not created:
            cartitem.quantity += 1
        else:
            cartitem.quantity = 1
        cartitem.save()

        serializer = CartSerializer(cart)

        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    
class UpdateItemQty(APIView):

    def put(self, request):

        cart_item_id = request.data.get('cart_item_id')
        quantity = request.data.get('quantity')

        cart_item = CartItems.objects.get(id=cart_item_id)
        cart_item.quantity = int(quantity)

        cart_item.save()

        serializer = CartItemSerializer(cart_item)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

class DeleteCartItem(APIView):

    def delete(self, request, pk):
        cart_item = CartItems.objects.get(pk=pk)
        cart_item.delete()

        return Response("Cart item deleted", status=status.HTTP_204_NO_CONTENT)
    
class AddReview(APIView):

    def post(self, request):
        product_id = request.data.get("product_id")
        email = request.data.get("email")
        rating =  request.data.get("rating")
        comment = request.data.get("review")

        product = Product.objects.get(id=product_id)
        user = User.objects.get(email=email)
        if Review.objects.filter(user=user, product=product).exists():
            return Response("Review already added", status=status.HTTP_400_BAD_REQUEST)

        review = Review.objects.create(user=user, product=product, rating=rating, review=comment)

        serializer = ReviewSerializer(review)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class UpdateOrDeleteReview(APIView):

    def put(self, request, pk):

        review = Review.objects.get(pk=pk)
        rating = request.data.get('rating')
        review_text = request.data.get('review')

        review.rating = rating
        review.review = review_text
        review.save()

        serializer = ReviewSerializer(review)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, pk):
        review = Review.objects.get(pk=pk)
        review.delete()

        return Response({"message":"Review deleted successfully"},status=status.HTTP_204_NO_CONTENT)
    
class AddToWishlist(APIView):

    def post(self, request):
        email = request.data.get('email')
        product_id = request.data.get('product_id')

        user = User.objects.get(email=email)
        product = Product.objects.get(id = product_id)

        wishlist = Wishlist.objects.filter(user=user, product=product)
        if wishlist:
            wishlist.delete()
            return Response("Wishlist deleted successfully", status=status.HTTP_204_NO_CONTENT)
        
        new_wishlist = Wishlist.objects.create(user=user, product=product)
        serializer = WishlistSerializer(new_wishlist)
        return Response(serializer.data)


