"""finalproject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from unicodedata import name
from xml.dom.minidom import Document
from django.contrib import admin
from django.urls import path, include
from core import views
from django.contrib.auth import views as auth_views
from core.restaurant import views as r_views
from core.driver import views as d_views, apis as d_apis
from django.conf import settings
from django.conf.urls.static import static

restaurant_urlpatterns = [
    path('', r_views.home, name="home"),
    path('restaurant_profile/', r_views.profilepage, name="restaurant_profile"),
    path('post_delivery/', r_views.post_delivery, name="post_delivery"),
    path('deliveries/current/', r_views.current_delivery_page, name="current_delivery"),
    path('deliveries/archived/', r_views.archived_delivery_page, name="archived_delivery"),
]

driver_urlpatterns = [
    path('', d_views.home, name="home"),
    path('delivery/available/', d_views.deliveries_available_page, name="deliveries_available"),
    path('api/available_deliveries/', d_apis.available_deliveries_api, name="available_deliveries"),
]

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home),

    path('driver/', include((driver_urlpatterns, 'driver'))),
    path('restaurant/', include((restaurant_urlpatterns, 'restaurant'))),
    
    path('signup/', views.signup),
    path('signin/', auth_views.LoginView.as_view(template_name="signin.html")),
    path('signout/', auth_views.LogoutView.as_view(next_page="/")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)