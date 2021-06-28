from collections import OrderedDict
from django.db.models import Q
from rest_framework import generics, serializers,exceptions
from rest_framework.relations import StringRelatedField
from .models import *
from django.db.models import Count,Avg
from core.serializers import BankCombinationsSerializer, BankSerializer, ChallengeSerializer
from core.models import Bank,BankCombinations

class BankSerializerForUser(serializers.HyperlinkedModelSerializer):
    
    class Meta:
        model = Bank
        fields = ['id','name','logo']

    def to_representation(self, instance):
        response = super().to_representation(instance)
        coefficients = self.context.get('coefficient')
        
        current_coefficient = 0
        for i in coefficients:
            if i.get('bank_id') == instance.id:
                current_coefficient = i.get('coefficient_avg')
                break
        if instance.logo:
            
            response['logo'] = 'https://brokeriq.com.au' + str(instance.logo.url)
        response['coefficient'] = current_coefficient
        return response
   
class ClientHistorySerializer(serializers.ModelSerializer):

    class Meta:
        model = ClientHistory
        fields = ['id','challenge','solution','challenge_name',]

class ClientHistoryOnlySolutionSerializer(serializers.ModelSerializer):

    class Meta:
        model = ClientHistory
        fields = ['solution',]

class BankCombinationsSerializerForUser(serializers.ModelSerializer):

    challenge = serializers.StringRelatedField()
    class Meta:
        model = BankCombinations
        fields = ['id','challenge','solution','coefficient','bank',]


"""  Clients flow """

class ClientDetailSerializer(serializers.ModelSerializer):
    """ Client detail view serializer """
    history = ClientHistorySerializer(many=True,read_only=True)

    class Meta:
        model = Clients
        fields = ['id','name','surname','email','phone','draft','best_matches','history','combinations']
        read_only_fields = ['best_matches','history']

    def to_representation(self, instance):
        res = super().to_representation(instance)
        
        if 'search' in self.context['request'].query_params :
            if len(instance.combinations):
                combinations = []
                s_w = self.context['request'].query_params.get('search')
                for comb in instance.combinations:
                    if s_w.lower() in [comb.get('challenge').lower(),comb.get('solution').lower()]:
                        combinations.append(OrderedDict(comb))
            res['combinations'] = combinations
        
        if instance.history:
            history_challenges = instance.history.values_list('challenge_id',flat=True).distinct()
            history = {}
            history['history'] = []
            for ch_id in history_challenges:
                history['history'].append({
                    "challenge_name":f"{Challenge.objects.get(id=ch_id).name}",
                    'id':ch_id,
                    })
                solution_list = [sol_n for sol_n in ClientHistory.objects.filter(client_id=instance.id,challenge_id=ch_id).values_list('solution',flat=True)]
                history['history'][-1].update(
                    {'solution':solution_list}
                )
                
            res['history'] = history['history']


            _ins_challenge_combs = []
            for challenge_id in history_challenges:
                if Challenge.objects.filter(id=challenge_id).exists():
                    _ins_challenge_combs.append(
                        {
                            'id':challenge_id,
                            "challenge_name":f"{Challenge.objects.get(id=ch_id).name}",

                        }
                    ) 

                    solution_list_two = [sol_n for sol_n in BankCombinations.objects.filter(challenge_id=challenge_id).values_list('solution',flat=True).distinct()]
                    _ins_challenge_combs[-1].update(
                        {'solution':solution_list_two}
                    )
                    
            res['challenges'] = _ins_challenge_combs
        
        return res
    

class ClientDeleteSerializer(serializers.ModelSerializer):

    """ Client delete serializer """
    class Meta:
        model = Clients
        fields = ['id']

class ClientUpdateSerializer(serializers.ModelSerializer):

    """ This serializer for the updateing clients data """
    history = ClientHistorySerializer(many=True,read_only=True)

    class Meta:
        model = Clients
        fields = ['id','name','surname','email','phone','draft','best_matches','history','combinations']
        read_only_fields = ['best_matches','history']

    def to_representation(self, instance):
        response = super().to_representation(instance)
        combinations = self.context.get('request').data.pop('combinations')

        bank_combs = BankCombinations.objects.filter(challenge_id__in=ClientHistory.objects.filter(client_id=instance.id).values_list('challenge',flat=True))

        updated_challenges = []
        for c in combinations:
            try:
                challenge = Challenge.objects.get(id=c.get('challenge'))
                updated_challenges.append(challenge.id)
            except:
                raise exceptions.ValidationError({'detail':"Challenge not found"})
            for s in c.get('solutions'):
                print(s , 'solllll')
                print(c.get('challenge') , 'chall')
                
                ClientHistory.objects.get_or_create(client_id=instance.id,challenge_id=challenge.id,solution=s,challenge_name=challenge.name)
            
            if ClientHistory.objects.filter(challenge_id=challenge.id).exclude(solution__in=c.get('solutions')).exists():
                for i in  ClientHistory.objects.filter(challenge_id=challenge.id).exclude(solution__in=c.get('solutions')):
                    i.delete()
            
        if ClientHistory.objects.exclude(challenge_id__in=updated_challenges).exists():

            for i  in ClientHistory.objects.exclude(challenge_id__in=updated_challenges):
                i.delete()

        solution_list = []
        for i in ClientHistory.objects.filter(client_id=instance.id).values_list('solution',flat=True):
            if i not in solution_list:
                solution_list.append(i) 
      	
	  
        bank_combs = bank_combs.filter(solution__in=solution_list).distinct()
        
     
        
        if ClientHistory.objects.filter(client_id=instance.id).count():
            history_challenges = instance.history.values_list('challenge_id',flat=True).distinct()
            history = {}
            history['history'] = []
            for ch_id in history_challenges:
                history['history'].append({
                    "challenge_name":f"{Challenge.objects.get(id=ch_id).name}",
                    'id':ch_id,
                    })
                solution_list = [sol_n for sol_n in ClientHistory.objects.filter(client_id=instance.id,challenge_id=ch_id).values_list('solution',flat=True)]
                history['history'][-1].update(
                    {'solution':solution_list}
                )
                
            response['history'] = history['history']


            _ins_challenge_combs = []
            for challenge_id in history_challenges:
                if Challenge.objects.filter(id=challenge_id).exists():
                    _ins_challenge_combs.append(
                        {
                            'id':challenge_id,
                            "challenge_name":f"{Challenge.objects.get(id=ch_id).name}",

                        }
                    ) 

                    solution_list_two = [sol_n for sol_n in BankCombinations.objects.filter(challenge_id=challenge_id).values_list('solution',flat=True).distinct()]
                    _ins_challenge_combs[-1].update(
                        {'solution':solution_list_two}
                    )
                    
            response['challenges'] = _ins_challenge_combs

        if bank_combs.count():
            banks_list = []
            banks = bank_combs.values('bank_id').annotate(coefficient_avg = Avg('coefficient')).order_by('-coefficient_avg').distinct()[:5]           
            
            for b in banks:
                banks_list.append(BankSerializerForUser(Bank.objects.get(id=b.get('bank_id')),context={'coefficient':banks}).data)
            

            response['combinations'] = []
            for i in bank_combs:
                response['combinations'].append(BankCombinationsSerializerForUser(BankCombinations.objects.get(id=i.id)).data)
            
           
            instance.combinations = response['combinations']            
            instance.best_matches = banks_list
            instance.save() 

        
        return response

class ClientCreateSerializer(serializers.ModelSerializer):

    """ This serializer for creating any client """
    class Meta:
        model = Clients
        fields = ['id','name','surname','email','phone','draft','best_matches','history','combinations']
        read_only_fields = ['best_matches','history']
    
    def to_representation(self, instance):
        response = super().to_representation(instance) 
        combinations = self.context.get('request').data.pop('combinations')

        for c in combinations:
            try:
                challenge = Challenge.objects.get(id=c.get('challenge'))
            except:
                raise exceptions.ValidationError({'detail':"Challenge not found"})
            for s in c.get('solutions'):
                ClientHistory.objects.create(client_id=instance.id,challenge_id=challenge.id,challenge_name=challenge.name,solution=s)

        bank_combs = BankCombinations.objects.filter(challenge_id__in=ClientHistory.objects.filter(client_id=instance.id).values_list('challenge',flat=True))

        solution_list = []
        for i in ClientHistory.objects.filter(client_id=instance.id).values_list('solution',flat=True):
        
            if i not in solution_list:
                solution_list.append(i) 
        
        bank_combs = bank_combs.filter(solution__in=solution_list).distinct()

        if bank_combs.count():
            banks_list = []
            banks = bank_combs.values('bank_id').annotate(coefficient_avg = Avg('coefficient')).order_by('-coefficient_avg').distinct()[:5]           
            print(banks,'banks')
            for b in banks:
                banks_list.append(BankSerializerForUser(Bank.objects.get(id=b.get('bank_id')),context={'coefficient':banks}).data)
            
            print(banks_list,'banks_list')

            response['combinations'] = []
            for i in bank_combs:
                response['combinations'].append(BankCombinationsSerializerForUser(BankCombinations.objects.get(id=i.id)).data)
            
            
            instance.combinations = response['combinations']            
            instance.best_matches = banks_list
            instance.save() 
        
        
        
        return response

class ClientListSerializer(serializers.ModelSerializer):

    history = ClientHistorySerializer(many=True,read_only=True)

    class Meta:
        model = Clients
        fields = ['id','name','surname','email','phone','draft','best_matches','history','combinations']
        read_only_fields = ['best_matches','history']


   
   
