from django.db import models
from accounts.models import User
from core.models import Challenge

 
class Clients(models.Model):

    broker = models.ForeignKey(User,on_delete=models.CASCADE,related_name='broker',null=True,blank=True)
    name = models.CharField(max_length=150,blank=True)
    surname = models.CharField(max_length=150,blank=True)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=50,blank=True)
    draft = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    best_matches = models.JSONField(null=True)
    combinations = models.JSONField(blank=True,null=True)



    def __str__(self):
        return f'{self.name} - {self.surname}'



class ClientHistory(models.Model):

    DELETED_PROPERTY = (
        ('deleted','deleted')
    )
    
    client = models.ForeignKey(Clients,on_delete=models.SET_NULL,null=True,related_name='history')
    challenge = models.ForeignKey(Challenge,on_delete=models.SET_NULL,null=True,blank=True,default=DELETED_PROPERTY[0])
    challenge_name = models.CharField(max_length=250,blank=True,null=True)
    solution = models.TextField(blank=True)


    def __str__(self):
        return f'{self.pk}'
