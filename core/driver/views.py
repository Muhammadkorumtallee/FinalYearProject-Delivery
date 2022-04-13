from django.conf import settings
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from pytz import timezone
from core.models import Delivery
from django.contrib import messages
from django.utils import timezone


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
            messages.success(request, 'Delivery Accepted')
            delivery.save()

        return redirect(reverse('driver:deliveries_available'))

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

        return render(request,'driver/complete_delivery.html')

    return render(request, 'driver/delivering_delivery.html', {
        "GOOGLE_API_MAP": settings.GOOGLE_API_MAP,
        "del": delivery
    })


@login_required(login_url="/signin/?next=/driver/")
def driver_profile(request):
    return render(request, 'driver/driver_profile.html')


@login_required(login_url="/signin/?next=/driver/")
def salary(request):
    deliveries = Delivery.objects.filter(
        driver=request.user.driver, status_of_delivery=Delivery.DELIVERY_DELIVERED)


    distance_traveled = round(sum(delivery.distance for delivery in deliveries),2)
    total = sum(delivery.price for delivery in deliveries)
    number_deliveries = len(deliveries)

    return render(request, 'driver/salary.html', {
        "total": total,
        "number_deliveries": number_deliveries,
        "distance_traveled": distance_traveled
    })

