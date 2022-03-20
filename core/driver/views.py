from django.conf import settings
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.http import JsonResponse



@login_required(login_url="/signin/?next=/driver/")
def home(request):
    return redirect(reverse('driver:deliveries_available'))


@login_required(login_url="/signin/?next=/driver/")
def deliveries_available_page(request):
    return render(request, 'driver/deliveries_available.html', {
        "GOOGLE_API_MAP": settings.GOOGLE_API_MAP
    })

