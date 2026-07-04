from django.urls import path
from .views import home, register_user, login_user, reception_dashboard, doctor_dashboard, register_patient, start_visit, triage, triage_dashboard

urlpatterns = [
    path('', home, name='home'),
    path('register/', register_user, name='register'),
    path("login/", login_user, name="login"),
    path("reception-dashboard/", reception_dashboard, name="reception_dashboard"),
    path("doctor-dashboard/", doctor_dashboard, name="doctor_dashboard"),
    path("register-patient/", register_patient, name="register_patient"),
    path("start-visit/", start_visit, name="start_visit"),
    path("triage_dashboard/", triage_dashboard, name="triage_dashboard"),
    path("triage/", triage, name="triage"),
    
]