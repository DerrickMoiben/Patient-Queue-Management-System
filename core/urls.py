from django.urls import path
from .views import home, register_user, login_user, reception_dashboard, doctor_dashboard

urlpatterns = [
    path('', home, name='home'),
    path('register/', register_user, name='register'),
    path("login/", login_user, name="login"),
    path("reception-dashboard/", reception_dashboard, name="reception_dashboard"),
    path("doctor-dashboard/", doctor_dashboard, name="doctor_dashboard"),
]