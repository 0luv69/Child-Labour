from django.urls import path
from .views import *


urlpatterns = [
    path('', index, name= 'home'),
    path('api', ComplaintApi.as_view(), name="complaintapi"),
    path('email-verify', email_verify_token, name="email_verify_token"),
    path('del-comp', delete_complain, name="delete_complain"),
    path('app-comp', aprove_complain, name="delete_complain"),


]