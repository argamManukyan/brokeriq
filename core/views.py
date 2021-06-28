from accounts.serializers import ResetPasswordSerializer
from rest_framework.parsers import MultiPartParser,FileUploadParser
from django.db.models import Q
from rest_framework.exceptions import AuthenticationFailed, ValidationError
from .serializers import *
from .models import *
from rest_framework.response import Response
from .serializers import *
from django.db.models import Count
from rest_framework import generics, permissions, status
from clients.pagination import CustomPagination

class ListAndCreateSolution(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Solution.objects.all()
    serializer_class = SolutionSerializer
    pagination_class = CustomPagination

    def get_permissions(self):
        if self.request.method == 'POST':
            self.permission_classes = [permissions.IsAdminUser]
        return super().get_permissions()

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=False):
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)

        else:
            errors_list = {}
            errors_list['detail'] = []
            for k,v in serializer.errors.items():
                errors_list['detail'].extend(v) 
            return Response(errors_list,status=status.HTTP_400_BAD_REQUEST)


class ReadAndChangeSolutionAPI(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAdminUser]
    serializer_class = SolutionSerializer
    lookup_field = 'pk'
    queryset = Solution.objects.all()

    def get_permissions(self):
        if self.request.method != 'GET':
            self.permission_classes = [permissions.IsAdminUser]
        return super().get_permissions()

    def update(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=False):
            serializer.save()
            return super().update(request,*args,**kwargs)

        else:
            errors_list = {}
            errors_list['detail'] = []
            for k,v in serializer.errors.items():
                errors_list['detail'].extend(v) 
            return Response(errors_list,status=status.HTTP_400_BAD_REQUEST)


def key_ordering(list_data):
    for i in list_data:
        return i


class ListAndCreateChallengeAPI(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ChallengeSerializer
    queryset = Challenge.objects.all()
    pagination_class = CustomPagination

    def get_permissions(self):
        if self.request.method == 'POST':
            self.permission_classes = [permissions.IsAdminUser]
        return super().get_permissions()

    def get_queryset(self):
        
        qs = self.queryset
        q_params = self.request.query_params
        
        if q_params.get('name') == 'ASC':
            qs = qs.order_by('name')
        if q_params.get('name') == 'DESC':
            qs = qs.order_by('-name')
        if q_params.get('id') == 'ASC':
            qs = qs.order_by('id')
        if q_params.get('id') == 'DESC':
            qs = qs.order_by('-id')
        
        if q_params.get('search'):
            search_data = q_params.get('search')
            qs = qs.filter(Q(name__icontains=search_data) | Q(challenge_combinations__solution__icontains=search_data) | Q(challenge_combinations__bank__name__icontains=search_data)).distinct()

        if self.request.user.ordering_challenge and not 'selected_ids' in q_params:

            """ This is the method, for sorting customization """

            ids = self.request.user.ordering_challenge
            qs = sorted(qs.all(), key=lambda x: ids.index(x.id))
        if 'selected_ids' in q_params:

            """ We use there eval for parsing str to array """
            ids = self.request.get_full_path().split('selected_ids=')[1]
            qs = qs.distinct() | Challenge.objects.filter(id__in=eval(ids)).distinct()
        return qs



    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=False):
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)

        else:
            errors_list = {}
         
            errors_list['detail'] = []
            for k,v in serializer.errors.items():
                print(k,v)
                errors_list['detail'].extend(v) 
            return Response(errors_list,status=status.HTTP_400_BAD_REQUEST)   
    
class ReadAndChangeChallengeAPI(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAdminUser]
    serializer_class = ChallengeSerializer
    queryset = Challenge.objects.all()
    lookup_field = 'pk'

    def get_permissions(self):

        if self.request.method == "PATCH":
            self.permission_classes = [permissions.IsAdminUser]
        elif self.request.method == "PUT":
            self.permission_classes = [permissions.IsAdminUser]
        elif self.request.method == 'DELETE' :
            self.permission_classes = [permissions.IsAdminUser]
        elif self.request.method == 'GET' :
            self.permission_classes = [permissions.IsAuthenticated]
        return super().get_permissions()

    def update(self, request, *args, **kwargs):
        if self.queryset.filter(id=kwargs.get('pk')).exists():
            serializer = self.serializer_class(instance=self.queryset.filter(id=kwargs.get('pk')).first(),data=request.data)
            if serializer.is_valid(raise_exception=False):
                serializer.save()
                return super().update(request,*args,**kwargs)

            else:
                errors_list = {}
                errors_list['detail'] = []
                for k,v in serializer.errors.items():
                    errors_list['detail'].extend(v) 
                return Response(errors_list,status=status.HTTP_400_BAD_REQUEST)
        return Response({"detail":'Challenge with this id is not found'},status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, *args, **kwargs):
        obj = self.get_object()
        serializer = self.get_serializer(obj,context={"search":request.query_params.get('search')})
        return Response(serializer.data,status=200)


class ListAndCreateBankAPI(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = CustomPagination
    serializer_class = BankListSerializer
    queryset = Bank.objects.all()

    def get_permissions(self):
        if self.request.method == 'POST':
            self.permission_classes = [permissions.IsAdminUser]
        return super().get_permissions()

    def get_queryset(self):
        qs = self.queryset
        if self.request.query_params.get('name') == 'ASC':
            qs = qs.order_by('name')
        if self.request.query_params.get('name') == 'DESC':
            qs = qs.order_by('-name')
        if self.request.query_params.get('id') == 'ASC':
            qs = qs.order_by('id')
        if self.request.query_params.get('id') == 'DESC':
            qs = qs.order_by('-id')
        if self.request.query_params.get('broker_line') == 'DESC':
            qs = qs.order_by('-broker_line')
        if self.request.query_params.get('broker_line') == 'ASC':
            qs = qs.order_by('broker_line')
        if self.request.query_params.get('search'):
            search_data = self.request.query_params.get('search')
            qs = qs.filter(name__icontains=search_data)
        if self.request.query_params.get('solutions_length') == 'DESC':
            qs = qs.annotate(solutions_length=Count('bank_combinations')).order_by('-solutions_length')
        if self.request.query_params.get('solutions_length') == 'ASC':
            qs = qs.annotate(solutions_length=Count('bank_combinations')).order_by('solutions_length')
        return qs.all()
    
    def create(self, request, *args, **kwargs):
        
        if not request.user.is_staff:
            raise AuthenticationFailed("Authentication credentials were not provided.")

        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid(raise_exception=False):
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)

        else:
            errors_list = {}
            errors_list['detail'] = []
            for k,v in serializer.errors.items():
                errors_list['detail'].extend(v) 
            return Response(errors_list,status=status.HTTP_400_BAD_REQUEST)     
    
class ReadAbdChangeBankAPI(generics.RetrieveUpdateDestroyAPIView):
    
    permission_classes = [permissions.IsAuthenticated]
    queryset = Bank.objects.all()
    serializer_class = BankSerializer
    lookup_field = 'pk'

    def get_permissions(self):
        if self.request.method != 'GET':
            self.permission_classes = [permissions.IsAdminUser]
        return super().get_permissions()

    def retrieve(self, request, *args, **kwargs):
        obj = self.get_object()
        serializer = self.get_serializer(obj,context={'search':request.query_params.get('search')})
        return super().retrieve(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        if self.queryset.filter(id=kwargs.get('pk')).exists():
            serializer = self.serializer_class(instance=self.queryset.filter(id=kwargs.get('pk')).first(),data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data,status=200)
            else:
                errors_list = {}
                errors_list['detail'] = []
                for k,v in serializer.errors.items():
                    errors_list['detail'].extend(v) 
                return Response(errors_list,status=status.HTTP_400_BAD_REQUEST)
        return Response({"detail":'Bank with this id is not found'},status=status.HTTP_400_BAD_REQUEST)


class BankCoefficientCreateAPI(generics.GenericAPIView):

    serializer_class = BankCombinationsCreateSerializer
    permission_classes = [permissions.IsAdminUser]
    def post(self,request):

        """ Example of create combination 
        
        {   
            "bank": 3,
            "challenge": 23,
            "solutions": [
                {"coefficient":5,"solution":"test 2"},{"coefficient":3,"solution": "test 4"}
            ]
            
        }
        
         """

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=200)


class BankCoefficientUpdateAPI(generics.GenericAPIView):
    
    serializer_class = BankCombinationsUpdateSerializer

    permission_classes = [permissions.IsAdminUser]
    def patch(self,request):
        
        """ Example of update combination 
        
        {
            "challenge":23,
            "bank":3,
            "solutions": [
                {"id":70,"solution":"text   92","coefficient":5}
            ]
        }
        
         """
       
        challenge_id = request.data.get('challenge')
        bank_id = request.data.get('bank')
        for i in request.data.get('solutions'):
            
            combination = BankCombinations.objects.get(id=i['id'])
            combination.challenge_id = challenge_id
            combination.solution = i['solution']
            combination.coefficient = i['coefficient']
            combination.save()

            if BankCombinations.objects.filter(bank_id=bank_id,challenge_id=challenge_id,solution=i['solution']).exclude(id=i['id']).exists():
                raise ValidationError({'detail':'This combination for that bank already exists'})
        return Response(status=200)
         
        
        
class BankCoefficientDestroyAPIView(generics.GenericAPIView):
    
    serializer_class = BankCombinationsDestroySerializer
    permission_classes = [permissions.IsAdminUser]

    def post(self, request, *args, **kwargs):
        """ example of delete solution
        "solutions": [
                17,18,19
            ]
        
         """
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        return Response(status=204)


class BankCombinationRemove(generics.GenericAPIView):
    serializer_class = RemoveBankCombinationSerializer
    permission_classes = [permissions.IsAdminUser]

    def post(self, request):

        """ Example of remove all section of bank combination with current challenge """
        bank_id = request.data.get('bank')
        challenge_id = request.data.get('challenge')

        try:
            bank = Bank.objects.get(id=bank_id)
            challenge = Challenge.objects.get(id=challenge_id)
            
        except Bank.ObjectDoesNotExist:
            return Response(status=400)
        except Challenge.ObjectDoesNotExist:
            return Response(status=400)

        combinations = BankCombinations.objects.filter(challenge_id=challenge_id,bank_id=bank_id)
        for i in combinations:
            i.delete()
        return Response(status=204)


class BankImageAPI(generics.GenericAPIView):

    serializer_class = BankImageSerializer
    parser_classes = [MultiPartParser, FileUploadParser]
    queryset = Bank.objects.all()
   
    def post(self,request,**kwargs):

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        id = request.data.get('id')
        image = request.FILES.get('image')
        
        bank = Bank.objects.get(id=id)

        if bank.logo:
            bank.logo.delete()
            bank.logo = image
            bank.save()
        else:
            bank.logo = image
            bank.save()

        return Response(status=201)

    def patch(self,request,**kwargs):

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        id = request.data.get('id')
        image = request.FILES.get('image')
        
        bank = Bank.objects.get(id=id)

        if bank.logo:
            bank.logo.delete()
            bank.logo = image
            bank.save()
        else:
            bank.logo = image
            bank.save()

        return Response(status=200)

    def delete(self,request,**kwargs):
        id = kwargs.get('pk')
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        bank = Bank.objects.get(id=id)
        bank.logo.delete()

        return Response(status=204)
