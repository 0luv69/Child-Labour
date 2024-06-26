from django.shortcuts import render, redirect, HttpResponse
from .models import *
from .serializers import *
from rest_framework.response import Response
from rest_framework.views import APIView
import random
from rest_framework.decorators import api_view

def index(request):
    if request.method == "POST":
        if request.GET.get('action') == 'delete':
            id = request.POST.get('del-id')
            Complaint.objects.get(id=id).delete()
            return redirect('home')
        elif request.GET.get('action') == 'approve':
            id = request.POST.get('del-id')
            complaint_obj= Complaint.objects.get(id=id)
            complaint_obj.admin_verified = True
            complaint_obj.save()
            return redirect('home')

    complaint = Complaint.objects.filter(admin_verified=False )
    return render(request, 'admin.html', context={'complaint':complaint})

class ComplaintApi(APIView):
    permission_classes = []
    authentication_classes = []
    def get(self , request):
        std_all_obj = Complaint.objects.all()
        serializer = CompSerializer(std_all_obj, many=True)
        return Response({
            'payload' : serializer.data,
            'Message': 'Success Fetched'
        },
        status=200)
    
    def post(self,request):
        data = request.data 
        email_token = str(random.randint(1000, 9999)) 
        data['email_token'] = email_token
        serializer = CompSerializer(data=data)
        if serializer.is_valid():
            complaint = serializer.save()

            send_account_activation_email(complaint.email, email_token, complaint)
            return Response({
                'posted':True,
                'id': complaint.id,
                'token': complaint.email_token,
            }, status=200)
        return Response({'posted':False,'error' : serializer.errors , 'message': 'Bad request here' }, status= 403,)


@api_view(['POST'])
def email_verify_token(request):
    data = request.data
    id = data.get('id')
    token = data.get('emailtoken')
    
    try:
        complaint_obj = Complaint.objects.get(id=id, email_token=token)
        complaint_obj.email_verified = True
        complaint_obj.save()
        return Response({
            'verified': True,
        }, status=200)
    except Complaint.DoesNotExist:
        return Response({
            'verified':False,
            'message': 'Invalid ID or token',
        }, status=403)
    except Exception as e:
        return Response({
            'verified':False,
            'message': f'An unexpected error occurred,{e}'
        }, status=500)
        
@api_view(['POST'])
def delete_complain(request):
    data = request.data
    id = data.get('id')
    email = data.get('email')
    try:
        complaint_obj = Complaint.objects.get(id=id, email=email)
        complaint_obj.delete()
        return Response({
            'deleted': True,
        }, status=200)
    except Complaint.DoesNotExist:
        return Response({
            'deleted':False,
            'message': 'Invalid ID or Email',
        }, status=403)
    except Exception as e:
        return Response({
            'deleted':False,
            'message': f'An unexpected error occurred,{e}'
        }, status=500)


       
@api_view(['POST'])
def aprove_complain(request):
    data = request.data
    id = data.get('id')
    email = data.get('email')
    try:
        complaint_obj = Complaint.objects.get(id=id,email = email)
        complaint_obj.admin_verified = True
        complaint_obj.save()
        return Response({
            'Aproved': True,
        }, status=200)
    except Complaint.DoesNotExist:
        return Response({
            'Aproved':False,
            'message': 'Invalid ID',
        }, status=403)
    except Exception as e:
        return Response({
            'Aproved':False,
            'message': f'An unexpected error occurred,{e}'
        }, status=500)

    
















def activate_email(request,emailtoken):
    try:
        user_profile= Complaint.objects.get(email_token=emailtoken) 
        user_profile.is_email_verified= True
        user_profile.save()
    except:
        return HttpResponse('Sorry but wrong authentation key,.....................................................')

    return redirect('/')