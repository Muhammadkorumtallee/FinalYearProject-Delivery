from django.conf import settings
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from core.models import Delivery
from django.contrib import messages


@login_required(login_url="/signin/?next=/driver/")
def home(request):
    return redirect(reverse('driver:deliveries_available'))


@login_required(login_url="/signin/?next=/driver/")
def deliveries_available_page(request):

    deliveries = Delivery.objects.filter(
        status_of_delivery__in=[Delivery.DELIVERY_POSTED]
    )

    #When driver accept delivery then status of delivery changes to delivering
    #delivery = Delivery.objects.filter(status_of_delivery=Delivery.DELIVERY_POSTED).last()
    
    if request.method == 'POST':
        delivery = get_object_or_404(Delivery, pk=request.POST.get('receipt_number'))
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
