from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from django.core.mail import send_mail
import random

# Create your models here.


class Complaint (models.Model):
    title = models.CharField(max_length=250)
    image = models.CharField( max_length=100)
    location = models.CharField( max_length=100)
    email = models.EmailField( max_length=250)
    description = models.TextField()
    Type_list = (
        ('sexual-abuse', 'Sexual Abuse'),
        ('forced-labor', 'Forced Labor'),
        ('domestic-servitude', 'Domestic Servitude'),
        ('agricultural-labor', 'Agricultural Labor'),
        ('industrial-work', 'Industrial Work'),
        ('mining', 'Mining'),
        ('street-work', 'Street Work'),
        ('bonded-labor', 'Bonded Labor'),
        ('child-soldiering', 'Child Soldiering'),
        ('trafficking', 'Trafficking'),
        ('informal-sector-work', 'Informal Sector Work'),
        ('construction-work', 'Construction Work'),
    )
    
    type = models.CharField( max_length=100, choices=Type_list, default= 'forced-labor')

    email_token = models.CharField(max_length=100, null= True, blank= True)
    email_verified = models.BooleanField(default=False)
    admin_verified = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    

# @receiver(post_save, sender= Complaint)
# def send_email_token(sender, instance, created, **kwargs):
#     try:
#         if created:
#             email_token = str(random.randint(1000, 9999))
#             email = instance.email 
#             Complaint.objects.filter(id=instance.id).update(email_token=email_token)
#             send_account_activation_email(email, email_token, instance)
#     except Exception as E:
#         print(E)

def send_account_activation_email(email, email_token, complaint_instance):
    subject= 'lets verify so click the link plz'
    email_from = settings.EMAIL_HOST_USER
    message = f'''Hi, {complaint_instance.email} Your authentation url is plz open to be verified user, thank
    click on the link to Activate Your account {email_token}
    thanks
'''

    send_mail(subject, message, email_from, [email])