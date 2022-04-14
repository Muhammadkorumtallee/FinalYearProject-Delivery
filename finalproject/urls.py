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
    path('driver_info/', d_views.driver_info, name="driver_info"),
    path('salary/', d_views.salary, name="salary"),
     path('deliveries_done/', d_views.deliveries_done, name="deliveries_done"),

    path('delivery/available/', d_views.deliveries_available_page, name="deliveries_available"),
    path('delivery/delivering/', d_views.delivering_delivery_page, name="delivering_delivery"),

    path('api/available_deliveries/', d_apis.available_deliveries_api, name="available_deliveries"),
    path('api/available_delivering/', d_apis.available_delivering_api, name="available_delivering"),
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