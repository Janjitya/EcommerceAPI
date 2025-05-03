from django.conf import settings
from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import AbstractUser

# Create your models here.

class CustomUser(AbstractUser):

    email = models.EmailField(unique=True)
    profile_pic_url = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.email
    
class Category(models.Model):
    category_name = models.CharField(max_length=100)
    slug = models.SlugField(blank=True, unique=True)

    def __str__(self):
        return self.category_name
    
    def save(self, *args, **kwargs):

        if not self.slug:
            self.slug = slugify(self.category_name)
            unique_slug = self.slug
            counter = 1
            while Category.objects.filter(slug=unique_slug).exists():
                unique_slug = f"{self.slug}-{counter}"
                counter += 1
            self.slug = unique_slug
        
        super().save(*args, **kwargs)

class Product(models.Model):

    product_name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    slug = models.SlugField(blank=True, unique=True)
    featured = models.BooleanField(default=False)
    image = models.ImageField(upload_to="products/images/", blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, blank=True, null=True, related_name='products')
    

    def __str__(self):
        return self.product_name
    
    def save(self, *args, **kwargs):

        if not self.slug:
            self.slug = slugify(self.product_name)
            unique_slug = self.slug
            counter = 1
            while Product.objects.filter(slug=unique_slug).exists():
                unique_slug = f"{self.slug}-{counter}"
                counter += 1
            self.slug = unique_slug
        
        super().save(*args, **kwargs)

class Cart(models.Model):
    cart_code = models.CharField(max_length=11, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.cart_code
    
class CartItems(models.Model):
    cart = models.ForeignKey(Cart, on_delete= models.CASCADE, related_name='cartitems')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='items')
    quantity = models.IntegerField(default=1)
    

    def __str__(self):
        return f"{self.quantity} x {self.product.product_name} in cart {self.cart.cart_code}"
    

class Review(models.Model):

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="reviews")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="reviews")
    rating = models.PositiveIntegerField()
    review = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['product', 'user']
        ordering = ['-created']

    def __str__(self):
        return f"{self.user.username} - {self.product.product_name} {self.rating}"            

class ProductRating(models.Model):
    product = models.OneToOneField(Product, on_delete=models.CASCADE, related_name="rating")
    average_rating = models.FloatField(default=0.0)
    total_rating = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.product.product_name} - {self.average_rating} ({self.total_rating} reviews)"
    
class Wishlist(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="wishlist")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="wishlist")
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['user', 'product']

    def __str__(self):
        return f"{self.user.username} - {self.product.product_name}"    
    