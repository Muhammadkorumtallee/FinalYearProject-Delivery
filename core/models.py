from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import uuid

class Restaurant(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    restaurant_address = models.CharField(max_length=255, blank=True)
    restaurant_address_latitude = models.FloatField(default=0)
    restaurant_address_longitude = models.FloatField(default=0)
    restaurant_avatar = models.ImageField(
        upload_to='restaurant/restaurant_avatar/', null=True, blank=True)

    def __str__(self):
        return self.user.get_full_name()

class Driver(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    latitude = models.FloatField(default=0)
    longitude = models.FloatField(default=0)

    def __str__(self):
        return self.user.get_full_name()

class Delivery(models.Model):
    DELIVERY_POSTING = "posting"
    DELIVERY_POSTED= "posted"
    DELIVERY_DELIVERING = "delivering"
    DELIVERY_DELIVERED = "delivered"
    DELIVERY_CANCELLED = "cancelled"
    STATUS_DELIVERY = (
        (DELIVERY_POSTING, "Posting"),
        (DELIVERY_POSTED, "Posted"),
        (DELIVERY_DELIVERING, "Delivering"),
        (DELIVERY_DELIVERED, "Delivered"),
        (DELIVERY_CANCELLED, "Cancelled"),
    )

    receipt_number = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    status_of_delivery = models.CharField(max_length=50, choices=STATUS_DELIVERY, default=DELIVERY_POSTING)
    address = models.CharField(max_length=255)
    information = models.CharField(max_length=255)
    posted_time = models.DateTimeField(default=timezone.now)

    #delivery latitude and longitude 
    delivery_address_latitude = models.FloatField(default=0)
    delivery_address_longitude = models.FloatField(default=0)

    #price
    duration = models.IntegerField(default=0)
    distance = models.FloatField(default=0)
    price = models.FloatField(default=0)

    #assign driver to delivery
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.address
