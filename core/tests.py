from django.test import TestCase
from django.contrib.auth.models import User
from core.restaurant.forms import DeliveriesCreateForm
from django.urls import reverse, resolve
from core.restaurant import views
from core.views import home
from core.restaurant.views import profilepage
from finalproject.urls import driver_urlpatterns


# testing if a user is created


class TestModel(TestCase):
    def testing_create_user(self):
        user = User.objects.create_user(
            first_name='testing', last_name='sample1', username='testinguser@app.com'
        )
        user.set_password('password123')
        user.save()
        self.assertEqual(str(user), 'testinguser@app.com')

    def testing_posting_deliveries(self):
        form = DeliveriesCreateForm(data={
            'address': 'Liffey Valley Shopping Centre',
            'information': 'leave outside',
            'delivery_address_latitude': 54,
            'delivery_address_longitude': 100,
        })

        self.assertTrue(form.is_valid())

    def testing_posting_deliveries_no_address(self):
        form = DeliveriesCreateForm(data={})

        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors), 3)

    def testing_url_homepage(self):
        url = reverse('home')
        self.assertEquals(resolve(url).func, home)

