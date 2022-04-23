from django.conf import settings
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from pytz import timezone
from core.models import Delivery
from django.contrib import messages
from django.utils import timezone
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from core.restaurant import forms


@login_required(login_url="/signin/?next=/driver/")
def home(request):
    return redirect(reverse('driver:deliveries_available'))


@login_required(login_url="/signin/?next=/driver/")
def deliveries_available_page(request):

    deliveries = Delivery.objects.filter(
        status_of_delivery__in=[Delivery.DELIVERY_POSTED]
    )

    # When driver accept delivery then status of delivery changes to delivering
    if request.method == 'POST':
        delivery = get_object_or_404(
            Delivery, pk=request.POST.get('receipt_number'))
        if delivery:
            delivery.status_of_delivery = Delivery.DELIVERY_DELIVERING
            delivery.driver = request.user.driver
            
            delivery.save()

        return render(request, 'driver/accepted_delivery.html')

    return render(request, 'driver/deliveries_available.html', {
        "GOOGLE_API_MAP": settings.GOOGLE_API_MAP,
        "del": deliveries
    })


@login_required(login_url="/signin/?next=/driver/")
def delivering_delivery_page(request):
    delivery = Delivery.objects.filter(
        driver=request.user.driver,
        status_of_delivery__in=[
            Delivery.DELIVERY_DELIVERING,
        ]
    ).last()

    if request.method == 'POST' and delivery.status_of_delivery == Delivery.DELIVERY_DELIVERING:
        delivery.status_of_delivery = Delivery.DELIVERY_DELIVERED
        delivery.delivered_time = timezone.now()
        delivery.save()

        return render(request, 'driver/complete_delivery.html')

    return render(request, 'driver/delivering_delivery.html', {
        "GOOGLE_API_MAP": settings.GOOGLE_API_MAP,
        "del": delivery
    })


@login_required(login_url="/signin/?next=/driver/")
def driver_info(request):
    user_form = forms.UserForm(instance=request.user)
    restaurant_form = forms.RestaurantForm(instance=request.user.restaurant)
    passwordchange_form = PasswordChangeForm(request.user)

    if request.method == "POST":

        passwordchange_form = PasswordChangeForm(request.user, request.POST)
        if passwordchange_form.is_valid():
            user = passwordchange_form.save()
            update_session_auth_hash(request, user)

            messages.success(request, 'Password Updated Successfull')
            return redirect(reverse('driver:driver_info'))

    return render(request, 'driver/driver_info.html',
                  {
                      "user_form": user_form,
                      "restaurant_form": restaurant_form,
                      "passwordchange_form": passwordchange_form
                  })


@login_required(login_url="/signin/?next=/driver/")
def salary(request):
    deliveries = Delivery.objects.filter(
        driver=request.user.driver, status_of_delivery=Delivery.DELIVERY_DELIVERED)

    distance_traveled = round(
        sum(delivery.distance for delivery in deliveries), 2)
    total = sum(delivery.price for delivery in deliveries)
    number_deliveries = len(deliveries)

    return render(request, 'driver/salary.html', {
        "total": total,
        "number_deliveries": number_deliveries,
        "distance_traveled": distance_traveled
    })


@login_required(login_url="/signin/?next=/driver/")
def deliveries_done(request):
    deliveries = Delivery.objects.filter(
        driver=request.user.driver, status_of_delivery=Delivery.DELIVERY_DELIVERED)

    return render(request, 'driver/deliveries_done.html', {
        "deliveries": deliveries
    })
