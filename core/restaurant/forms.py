import dis
from django.contrib.auth.models import User
from django import forms

from core.models import Restaurant, Delivery


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = {
            'first_name',
            'last_name'
        }


class RestaurantForm(forms.ModelForm):
    class Meta:
        model = Restaurant
        fields = ('restaurant_avatar',
                  'restaurant_address',
                  'restaurant_address_latitude',
                  'restaurant_address_longitude',
                  )


class DeliveriesCreateForm(forms.ModelForm):
    address = forms.CharField(required=True)
    information = forms.CharField(required=False)

    class Meta:
        model = Delivery
        fields = (
            'address',
            'information',
            'delivery_address_latitude',
            'delivery_address_longitude',
        )
