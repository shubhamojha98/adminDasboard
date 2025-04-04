from django.urls import path
from .views.login_view import login_view

from .views.dashboard_view import dashboard_view
from .views.property_view import property_view
from .views.water_view import water_view
from .views.waste_view import waste_view

urlpatterns = [
    path("", login_view, name="login"),
    path("dashboard/", dashboard_view, name="dashboard"),
    path("property/", property_view, name="property"),
    path("water/", water_view, name="water"),
    path("waste/", waste_view, name="waste"),
]
