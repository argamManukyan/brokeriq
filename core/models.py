from django.db import models
from django.forms import model_to_dict
from smart_selects.db_fields import ChainedForeignKey
from channels.layers import get_channel_layer
from django.db.models.signals import post_delete, post_save
from asgiref.sync import async_to_sync
from accounts.models import Notifications

channel_layer = get_channel_layer()

class Challenge(models.Model):
    name = models.CharField(max_length=150,unique=True,
    error_messages={
        'unique':'Challenge with this name already exists'
        }
    )

    def __str__(self):
        return "%s" %self.name


class Solution(models.Model):
    
    name = models.TextField(unique=True,error_messages={
        'unique':'Solution with this name already exists'
    })

    def __str__(self):
        return self.name


class Bank(models.Model):
    name = models.CharField(max_length=150,unique=True,error_messages={
        'unique':'Bank with this name already exists'
    })
    logo = models.ImageField(blank=True)
    web_page = models.URLField(unique=True,error_messages={
        'unique':'Bank with this web page already exists'
    })
    broker_line = models.CharField(max_length=50,blank=True)
    email = models.EmailField(blank=True)

    def __str__(self):
        return self.name


class BankCombinations(models.Model):
    bank = models.ForeignKey(Bank, on_delete=models.CASCADE,related_name='bank_combinations')
    challenge = models.ForeignKey(Challenge,on_delete=models.CASCADE,null=True,blank=True,related_name='challenge_combinations')
    solution = models.TextField(blank=True)
    coefficient = models.FloatField(null=True,blank=True)

    def __str__(self):
        return str(self.pk)


def post_save_solution(sender,created,instance,*args,**kwargs):
        
    if created:
        title = f'A new solution "{instance.solution}" has been created'
        notify = Notifications.objects.create(title=title,type='success')
       
        async_to_sync(channel_layer.group_send)(
            'notify',
            {'type':'send_data','text':model_to_dict(notify)}
        )
    else:
        title = f'A  solution "{instance.solution}" has been updated'
        notify = Notifications.objects.create(title=title,type='info')
        async_to_sync(channel_layer.group_send)(
            'notify',
            {'type':'send_data','text':model_to_dict(notify)}
        )
    
post_save.connect(post_save_solution,sender=BankCombinations)


def post_delete_solution(sender,instance,**kwargs):

    title = f'A solution "{instance.solution}" has been deleted'
    notify = Notifications.objects.create(title=title,type='warning')
    async_to_sync(channel_layer.group_send)(
        'notify',
        {'type':'send_data','text':model_to_dict(notify)}
    )    

post_delete.connect(post_delete_solution,sender=BankCombinations)





def post_save_challenge(sender,created,instance,*args,**kwargs):
        
    if created:
        title = f'A new challenge "{instance.name}" has been created'
        notify = Notifications.objects.create(title=title,type='success')
       
        async_to_sync(channel_layer.group_send)(
            'notify',
            {'type':'send_data','text':model_to_dict(notify)}
        )
    else:
        title = f'A  challenge "{instance.name}" has been updated'
        notify = Notifications.objects.create(title=title,type='info')
        async_to_sync(channel_layer.group_send)(
            'notify',
            {'type':'send_data','text':model_to_dict(notify)}
        )
    
post_save.connect(post_save_challenge,sender=Challenge)


def post_delete_challenge(sender,instance,**kwargs):

    title = f'A challenge "{instance.name}" has been deleted'
    notify = Notifications.objects.create(title=title,type='warning')
    async_to_sync(channel_layer.group_send)(
        'notify',
        {'type':'send_data','text':model_to_dict(notify)}
    )    

post_delete.connect(post_delete_challenge,sender=Challenge)



def post_save_banks(sender,created,instance,*args,**kwargs):
        
    if created:
        title = f'A new bank "{instance.name}" has been created'
        notify = Notifications.objects.create(title=title,type='success')
       
        async_to_sync(channel_layer.group_send)(
            'notify',
            {'type':'send_data','text':model_to_dict(notify)}
        )
    else:
        title = f'A  bank "{instance.name}" has been updated'
        notify = Notifications.objects.create(title=title,type='info')
        async_to_sync(channel_layer.group_send)(
            'notify',
            {'type':'send_data','text':model_to_dict(notify)}
        )
    
post_save.connect(post_save_banks,sender=Bank)


def post_delete_bank(sender,instance,**kwargs):

    title = f'A bank "{instance.name}" has been deleted'
    notify = Notifications.objects.create(title=title,type='warning')
    async_to_sync(channel_layer.group_send)(
        'notify',
        {'type':'send_data','text':model_to_dict(notify)}
    )    

post_delete.connect(post_delete_bank,sender=Bank)