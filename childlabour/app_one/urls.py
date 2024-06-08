from django.urls import path
from .views import *


urlpatterns = [
    path('api', ComplaintApi.as_view(), name="complaintapi"),
    path('email_verify', email_verify_token, name="email_verify_token"),


]