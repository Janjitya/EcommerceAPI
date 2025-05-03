from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.db.models import Avg
from .models import Review, ProductRating

@receiver(post_save, sender=Review)
def update_product_rating_on_save(sender, instance, **kwargs):
    product = instance.product
    reviews = Review.objects.all()
    total_reviews = reviews.count()

    review_average = reviews.aggregate(Avg('rating'))['rating__avg'] or 0.0

    product_rating, created = ProductRating.objects.get_or_create(product=product)
    product_rating.average_rating = review_average
    product_rating.total_rating = total_reviews
    product_rating.save()

@receiver(post_delete, sender=Review)
def update_product_rating_on_delete(sender, instance, **kwargs):
    product = instance.product
    reviews = Review.objects.all()
    total_reviews = reviews.count()

    review_average = reviews.aggregate(Avg('rating'))['rating__avg'] or 0.0

    product_rating, created = ProductRating.objects.get_or_create(product=product)
    product_rating.average_rating = review_average
    product_rating.total_rating = total_reviews
    product_rating.save()


