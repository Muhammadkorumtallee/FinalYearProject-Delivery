from django.conf import settings
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from core.restaurant import forms
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages
from core.models import Delivery, Restaurant
import requests

@login_required
def home(request):
    return redirect(reverse('restaurant:restaurant_profile'))

@login_required(login_url="/signin/?next=/restaurant/")
def profilepage(request):
    user_form = forms.UserForm(instance=request.user)
    restaurant_form = forms.RestaurantForm(instance=request.user.restaurant)
    passwordchange_form = PasswordChangeForm(request.user)

    if request.method == "POST":
        if request.POST.get('task') == 'profile_update':
            user_form = forms.UserForm(request.POST, instance=request.user)
            restaurant_form = forms.RestaurantForm(request.POST, request.FILES, instance=request.user.restaurant)

            if restaurant_form.is_valid() and user_form.is_valid():
                user_form.save()
                restaurant_form.save()
                return redirect(reverse('restaurant:restaurant_profile'))

        elif request.POST.get('task') == 'password_update':
            passwordchange_form = PasswordChangeForm(request.user, request.POST)
            if passwordchange_form.is_valid():
                user = passwordchange_form.save()
                update_session_auth_hash(request, user)

                messages.success(request, 'Password Updated Successfull')
                return redirect(reverse('restaurant:restaurant_profile'))

    return render(request, 'restaurant/restaurant_profile.html',
    {
        "user_form": user_form,
        "restaurant_form": restaurant_form,
        "passwordchange_form": passwordchange_form
    })

@login_required(login_url="/signin/?next=/restaurant/")
def post_delivery(request):
    deliverypost_form = forms.DeliveriesCreateForm()
    restaurant_here = Restaurant.objects.first()
    store_restaurant_address = restaurant_here.restaurant_address
    posts = Delivery.objects.filter(restaurant=request.user.restaurant, status_of_delivery=Delivery.DELIVERY_POSTED).all()
    if request.method == "POST":
        deliverypost_form = forms.DeliveriesCreateForm(request.POST)
        if deliverypost_form.is_valid(): 
            posting_delivery = deliverypost_form.save(commit=False)
            posting_delivery.restaurant = request.user.restaurant
            posting_delivery.status_of_delivery = Delivery.DELIVERY_POSTED              #change status of delivery
            posting_delivery.restaurant_address_lat = request.user.restaurant.restaurant_address_latitude
            posting_delivery.restaurant_address_lng = request.user.restaurant.restaurant_address_longitude
            

            try:
                r = requests.get("https://maps.googleapis.com/maps/api/distancematrix/json?origins={}&destinations={}&mode=driving&key={}".format(
                    store_restaurant_address,
                    posting_delivery.address,
                    settings.GOOGLE_API_MAP,
                ))

                print(r.json()['rows'])
                distance = r.json()['rows'][0]['elements'][0]['distance']['value']
                duration = r.json()['rows'][0]['elements'][0]['duration']['value']
                posting_delivery.distance = round(distance/1000, 2)
                posting_delivery.duration = int(duration/60)

                if posting_delivery.distance <= 2:
                    posting_delivery.price = 2
                elif  posting_delivery.distance > 2 and posting_delivery.distance <= 4:
                    posting_delivery.price = 3
                else:
                    posting_delivery.price = 5

                posting_delivery.save()  
            except Exception as e:
                print(e)
                messages.error(request, "Sorry no price availabe")

            return redirect(reverse('restaurant:post_delivery'))

    return render(request, 'restaurant/post_delivery.html', {
        'deliverypost_form': deliverypost_form, 
        "posting": posts,
        "GOOGLE_API_MAP": settings.GOOGLE_API_MAP,})
        
@login_required(login_url="/sign-in/?next=/restaurant/")
def current_delivery_page(request):
    deliveries = Delivery.objects.filter(
        restaurant = request.user.restaurant,
        status_of_delivery__in=[
            Delivery.DELIVERY_DELIVERING,
            Delivery.DELIVERY_POSTED
        ]
    )
        
    if request.method == 'POST':
        delivery = get_object_or_404(Delivery, pk=request.POST.get('receipt_number'))
        if delivery:
            delivery.status_of_delivery = Delivery.DELIVERY_CANCELLED
            delivery.save()

    return render(request, 'restaurant/deliveries.html',
    {
        "deliveries": deliveries
    })

@login_required(login_url="/sign-in/?next=/restaurant/")
def archived_delivery_page(request):
    deliveries = Delivery.objects.filter(
        restaurant = request.user.restaurant,
        status_of_delivery__in=[
            Delivery.DELIVERY_DELIVERED,
            Delivery.DELIVERY_CANCELLED
        ]
    )

    return render(request, 'restaurant/deliveries.html',
    {
        "deliveries": deliveries
    })