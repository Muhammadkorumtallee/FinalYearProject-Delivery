
from django.http import JsonResponse
from pytz import timezone
from core.models import Delivery
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required


@csrf_exempt
@login_required(login_url="/driver/signin/")
def available_deliveries_api(request):
    delivery_all = list(Delivery.objects.filter(
        status_of_delivery=Delivery.DELIVERY_POSTED).values())

    return JsonResponse({
        "success": True,
        "deliveries": delivery_all
    })


@csrf_exempt
@login_required(login_url="/driver/signin/")
def available_delivering_api(request):

    delivering_all = list(Delivery.objects.filter(
        status_of_delivery=Delivery.DELIVERY_DELIVERING).values())

    return JsonResponse({
        "success": True,
        "delivering": delivering_all
    })