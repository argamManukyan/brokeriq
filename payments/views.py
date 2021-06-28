from django.conf import settings
from django.views import generic
import stripe,json
from django.views.decorators.csrf import csrf_exempt
from decouple import config
from django.http import JsonResponse
from rest_framework import exceptions, generics, permissions, views
from rest_framework.response import Response
from stripe.api_resources import payment_intent
from .models import UserPayments
from django.contrib.sites.shortcuts import get_current_site
from accounts.models import  User
from .serializers import *
from clients.pagination import CustomPagination
from rest_framework.decorators import api_view

stripe.api_key = settings.STRIPE_SECRET_KEY


def create_customer(user):
    customer = stripe.Customer.create(
        name=f'{user.first_name}',
        email=f'{user.email}',
        description="My First Test Customer Argam Manukyan",
    )
    return customer


def get_customer(request):
    if len(request.user.customer_id) > 1:
        customer = stripe.Customer.retrieve(id=request.user.customer_id)

    else:
        customer = create_customer(request.user)
        _user = User.objects.get(id=request.user.id)
        _user.customer_id = customer.get('id')
        _user.save(force_update=True)

    return customer


class FetchPlansAPI(views.APIView):

    def get(self,request,**kwargs):

        data = {}
        data['products'] = []


        products = stripe.Product.list(limit=20)['data']

        for pr in products:
            price = stripe.Price.list(product=pr)
            pr.update({"price":price['data']})
            data['products'].append(pr)

        return JsonResponse(data['products'],safe=False)


class CustomerDetailsAPI(views.APIView):

    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, **kwargs):


        try:
            customer = get_customer(request)
            payment_methods = stripe.PaymentMethod.list(
                customer=customer.id,  
                type="card",
            )
            
                           
            subscription = stripe.Subscription.list(customer=customer.id)
            
            data = {}
            data['customer'] = customer
            data['customer'].update({'payment_methods': payment_methods})
            data['customer'].update({'subscription': subscription})
            return JsonResponse(data, safe=False)
        except:
            return Response({'detail': 'Oops ! Something went wrong'}, status=400)


class AddPaymentAPI(generics.GenericAPIView):
    """ This endpoint for adding a payment method

        example of request 

        card={
          "number": "4242424242424242",
          "exp_month": 6,
          "exp_year": 2022,
          "cvc": "314",
        },

    """
    serializer_class = AddPaymentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):

        customer = get_customer(request)
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        if len(stripe.PaymentMethod.list(customer=customer.get('id'), type="card",).get('data')) > 0:
            new_payment = stripe.PaymentMethod.create(
                type='card',
                card=serializer.data
            )
            try:
                stripe.PaymentMethod.attach(new_payment.get('id'),customer=customer.get('id'))
                return Response(status=200,data={"success":'Payment default created'})

            except:
                return Response(status=400,data='Oops! Something went wrong')


        try:
            new_payment = stripe.PaymentMethod.create(
                type='card',
                card=serializer.data
            )

            customer.update(
                invoice_settings={
                    'default_payment_method': new_payment.get('id')
                }
            )

            return Response(status=200,data={"success":'Payment default created'})

        except:
            return Response(status=400,data='Oops! Something went wrong')


class DeletePaymentAPI(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = DeletePaymentSerializer

    def post(self,request,**kwargs):

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        try:
            stripe.PaymentMethod.detach(
            serializer.data.get('payment_method_id')
            )
            return Response(status=204)
        except:
            return Response({'detail':'Oops! Something went wrong'},status=400)


class ChangeDefaultPayment(generics.GenericAPIView):

    serializer_class = ChangeDefaultPaymentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        data = request.data
        serializer = self.serializer_class(data=data)
        serializer.is_valid(raise_exception=True)
        try:
            stripe.Customer.modify(
                data['customer_id'],
                invoice_settings={
                    'default_payment_method': data['payment_method_id'],
                },
            )
            return Response(status=200)
        except:
            return Response({'detail':'Oops! Something went wrong'},status=400)


class MakePayments(generics.GenericAPIView):

    """ Endpoint for a request a payment making  """

    serializer_class = MakePaymentsSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):

        customer = get_customer(request)

        tarrif_plan_id = request.data.get('tariff_id')

        try:
            tariff = Tarifs.objects.get(id=tarrif_plan_id)
        except:
            raise exceptions.NotFound({'detail': 'Plan is not found'})

        try:

            intent = stripe.PaymentIntent.create(
                amount=int(tariff.price * 100),
                currency='usd'
            )
            return JsonResponse({
                'clientSecret': intent['client_secret']
            })
        except Exception as e:
            return JsonResponse(error=str(e))


class CreateSubscriptionAPI(generics.GenericAPIView):
    # permission_classes = [permissions.IsAuthenticated]
    serializer_class = CreateSubscriptionSerializer

    def post(self, request, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        try:
            subscription = stripe.Subscription.create(
                customer=get_customer(request).id,
                items=[
                    {
                        'price': serializer.data['price_id']
                    }
                ],
                expand=['latest_invoice.payment_intent'],
            )

            print(subscription['latest_invoice']['paid'])
            if subscription['latest_invoice']['paid'] == True:
                request.user.scribed = True
                print('ok')
                request.user.tariff = stripe.Product.retrieve(subscription['items']['data'][0]['price']['product'])['name']
                request.user.save()
            return JsonResponse(subscription)
        except Exception as e:
            print(e)
            return Response(status=400)


class UnSubscribeAPI(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UnsubscribeSerializer

    def post(self,request,**kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            subs_cancel = stripe.Subscription.delete(serializer.data.get('subscription_id'))
            
            plan_name = stripe.Product.retrieve(subs_cancel['items']['data'][0]['price']['product'])['name']
            UserPayments.objects.create(user_id=request.user.id,reason=request.data.get('reason'),plan_name=plan_name,status=subs_cancel['status'],last_four=' ')
            request.user.scribed = False
            request.user.save()
            return Response(status=204)
        except:
            raise exceptions.ValidationError({'detail':'Subscription with given id does not exists'})


class ChangeSubscriptionAPI(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ChangeSubscriptionSerializer

    def post(self,request,**kwargs):

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            
            stripe.Subscription.delete(serializer.data.get('subscription_id'))

            subscription = stripe.Subscription.create(
                customer=get_customer(request).id,
                items=[
                    {
                        'price': serializer.data['price_id']
                    }
                ],
                expand=['latest_invoice.payment_intent'],
            )

            if subscription['latest_invoice']['paid'] == True:
                request.user.scribed = True
                request.user.tariff = stripe.Product.retrieve(subscription['items']['data'][0]['price']['product'])['name']
                request.user.save()
            return JsonResponse(subscription)
        
        except:
            raise exceptions.ValidationError({'detail':'Oops ! something went wrong'})

        
class FetchPaymentsAPi(views.APIView):
    
    def get(self,request,**kwargs):
        
        """starting_after is a id of last card and limit is a count cards per page"""
        # customer = get_customer(request)
        payments = stripe.PaymentIntent.list(customer='cus_JZJehkrPjI0Zlp',limit=3,starting_after='pi_1IwMiwGoRjiAlQgmYINufbhY',filter={''})
        print(payment_intent)
        return Response(payments['data'],status=200)


class UserPaymentHistoryAPI(generics.ListAPIView):

    serializer_class = UserPaymentsSerializer      
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = CustomPagination

    def get_queryset(self):
        
        query_params = self.request.query_params
        qs = UserPayments.objects.filter(user_id=self.request.user.id)
        
        if query_params.get('id') == 'ASC':
            qs = qs.order_by('id')
        if query_params.get('id') == 'DESC':
            qs = qs.order_by('-id')
        if query_params.get('card') == 'ASC':
            qs = qs.order_by('card')
        if query_params.get('card') == 'DESC':
            qs = qs.order_by('-card')
        if query_params.get('amount') == 'ASC':
            qs = qs.order_by('amount')
        if query_params.get('amount') == 'DESC':
            qs = qs.order_by('-amount')
        if query_params.get('plan_name') == 'ASC':
            qs = qs.order_by('plan_name')
        if query_params.get('plan_name') == 'DESC':
            qs = qs.order_by('-plan_name')
        if query_params.get('status') == 'ASC':
            qs = qs.order_by('status')
        if query_params.get('status') == 'DESC':
            qs = qs.order_by('-status')
        
        if query_params.get('from_date'):
            qs = qs.filter(created__gte=query_params.get('from_date'))
        if query_params.get('to_date'):
            qs = qs.filter(created__lte=query_params.get('to_date'))
        

        return qs

    

@csrf_exempt
@api_view(['POST'])
def my_webhook_view(request):
    payload = request.body
    event = None

    try:
        event = stripe.Event.construct_from(
        json.loads(payload), stripe.api_key
        )
    except ValueError as e:
    # Invalid payload
        return Response(status=400)

    # Handle the event

    if event.type == 'customer.subscription.deleted':
       
        data = event.data.object

        invoice = stripe.Invoice.retrieve(data['latest_invoice'])
        user_email = invoice['customer_email']
        plan_name = stripe.Product.retrieve(data['plan']['product'])['name']
        status = data['status']
        payment_intent = stripe.PaymentIntent.retrieve(invoice['payment_intent'])['charges']['data'][0]['payment_method_details']['card']['brand'].upper() + " **** **** **** " + str(stripe.PaymentIntent.retrieve(invoice['payment_intent'])['charges']['data'][0]['payment_method_details']['card']['last4'])
        us_pay = UserPayments.objects.create(plan_name=plan_name,status=status.lower() ,last_four=payment_intent,amount=int(int(data['items']['data'][0]['price']['unit_amount']) / 100))
        us_pay.user_id = User.objects.get(email=user_email).id
        us_pay.save()
        user = User.objects.get(email=user_email)
        user.scribed = False
        user.save(force_update=True)
        
    if event.type == "payment_intent.payment_failed" :

        data = event.data.object
        user_email = stripe.Customer.retrieve(data['customer'])['email']
        plan_name = 'Card connection'
        status = 'Failed'.lower() 
        payment_intent = str(data['last_payment_error']['payment_method']['card']['brand']).upper() + " **** **** **** " + str(data['last_payment_error']['payment_method']['card']['last4'])
        us_pay = UserPayments.objects.create(plan_name=plan_name,status=status,last_four=payment_intent,amount=int(int(data['amount']) / 100))
        us_pay.user_id = User.objects.get(email=user_email).id
        us_pay.save()

    if event.type == 'invoice.payment_failed':
        print('payment_failed - invoice')
        data = event.data.object
        user_email = data['customer_email']
        plan_name = stripe.Product.retrieve(data['lines']['data'][0]['plan']['product'])['name']
        status = data['status']
        payment_intent = str(stripe.PaymentIntent.retrieve(data['payment_intent'])['charges']['data'][0]['payment_method_details']['card']['brand']).upper() + " **** **** **** " + str(stripe.PaymentIntent.retrieve(data['payment_intent'])['charges']['data'][0]['payment_method_details']['card']['last4'])
        us_pay = UserPayments.objects.create(plan_name=plan_name,status=status.lower() ,last_four=payment_intent,amount=int(int(data['total']) / 100))
        us_pay.user_id = User.objects.get(email=user_email).id
        us_pay.save()
        
    elif event.type == 'invoice.paid':
        
        data = event.data.object

        user_email = data['customer_email']
        user = User.objects.get(email=user_email)
        user.scribed = True
        user.save()
        plan_name = stripe.Product.retrieve(data['lines']['data'][0]['plan']['product'])['name']
        status = data['status']
        payment_intent = str(stripe.PaymentIntent.retrieve(data['payment_intent'])['charges']['data'][0]['payment_method_details']['card']['brand']).upper() + " **** **** **** " + str(stripe.PaymentIntent.retrieve(data['payment_intent'])['charges']['data'][0]['payment_method_details']['card']['last4'])
        us_pay = UserPayments.objects.create(plan_name=plan_name,status=status.lower(),last_four=payment_intent,amount=int(int(data['amount_paid']) / 100))
        us_pay.user_id = user.id
        us_pay.save()
     

    else:
        print('Unhandled event type {}'.format(event.type))

    return Response(status=200)



class ChangeOrderingChallenges(generics.GenericAPIView):

    serializer_class = OrderingChallengeSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self,request,**kwargs):
        
        ordering_list = request.data.get('ordering')
        user = request.user
        user.ordering_challenge = ordering_list
        user.save()
        return Response(status=200,data={"success":"Ordering successfully created"})


# class GraphsAPI()