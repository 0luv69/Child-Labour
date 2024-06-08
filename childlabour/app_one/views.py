from django.shortcuts import render, redirect, HttpResponse, HttpResponseRedirect
from .models import *

# Create your views here.


def activate_email(request,emailtoken):
    try:
        user_profile= Complaint.objects.get(email_token=emailtoken) 
        user_profile.is_email_verified= True
        user_profile.save()
    except:
        return HttpResponse('Sorry but wrong authentation key,.....................................................')

    return redirect('/')