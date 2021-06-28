from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class UserPayments(models.Model):

    user = models.ForeignKey(User,on_delete=models.SET_NULL,null=True,blank=True)
    plan_name = models.CharField(max_length=120)
    reason = models.JSONField(null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=100)
    amount = models.IntegerField(default=0)
    last_four = models.CharField(max_length=10)

    
    def __str__(self):
        return str(self.pk)
