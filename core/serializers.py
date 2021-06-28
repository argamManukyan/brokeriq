from django.core.validators import FileExtensionValidator
from rest_framework import serializers,exceptions
from .models import *
from django.contrib.auth import get_user_model
from django.contrib.sites.shortcuts import get_current_site
from django.db.models import Q


User = get_user_model()

class SolutionSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Solution
        fields = "__all__"    


class BankCombinationsForChallengeSerializer(serializers.ModelSerializer):

    class Meta:
        model = BankCombinations
        fields = ['bank','solution','coefficient']


class ChallengeSerializer(serializers.ModelSerializer):

    
    class Meta:
        model = Challenge
        fields = ["id","name",'challenge_combinations']
        read_only_fields = ['challenge_combinations']

    def to_representation(self, instance):
        res =  super().to_representation(instance)
        comb_ids = instance.challenge_combinations.values('solution').distinct()
        combinations_arr = []
        for i in comb_ids:
            combinations_arr.append(BankCombinationsForChallengeSerializer(instance.challenge_combinations.filter(solution=i['solution']).first()).data)
        res['challenge_combinations'] = combinations_arr
        return res
        
    
class BankCombinationsSerializer(serializers.ModelSerializer):
    

    class Meta:
        model = BankCombinations
        fields = ['id','challenge','solution','coefficient','bank',]


class BankCombinationsCreateSerializer(serializers.Serializer):
    

    bank = serializers.IntegerField()
    challenge = serializers.IntegerField()
    solutions = serializers.ListField()
    
    
    def create(self, validated_data):
        solutions = validated_data.pop('solutions')

        bank_id = validated_data.pop('bank')
        challenge_id = validated_data.pop('challenge')

       
        for i in solutions:
            validated_data['solution'] = i.get('solution')
            
            if BankCombinations.objects.filter(challenge_id=challenge_id,bank_id=bank_id,solution=i.get('solution')).exists():
                raise exceptions.ValidationError({'detail':f'Combination with this data ({i.get("solution")}) already exists'})
            validated_data['coefficient'] = i.get('coefficient')
            validated_data['bank_id'] = bank_id
            validated_data['challenge_id'] = challenge_id
            BankCombinations.objects.create(**validated_data)
        return validated_data


class BankCombinationsUpdateSerializer(serializers.Serializer):
    

    bank = serializers.IntegerField()
    challenge = serializers.IntegerField()
    solutions = serializers.ListField(child=serializers.JSONField())
        
class RemoveBankCombinationSerializer(serializers.Serializer):


    bank = serializers.IntegerField()
    challenge = serializers.IntegerField()
    

class BankCombinationsUpdateSerializer(serializers.Serializer):


    bank = serializers.IntegerField()
    challenge = serializers.IntegerField()
    solutions = serializers.ListField(child=serializers.JSONField())
        

class BankCombinationsDestroySerializer(serializers.Serializer):

    solutions = serializers.ListField()
    

    def validate(self, attrs):
        solutions = attrs.get('solutions')

        for i in solutions:
            try:
                combination = BankCombinations.objects.get(id=i)
                combination.delete()
            except BankCombinations.DoesNotExist:
                raise exceptions.ValidationError({'detail':f'Combination with the id {i} does not exists'})
            except:
                 raise exceptions.ValidationError({'detail':'Oops! Something went wrong'})
        return super().validate(attrs)


class BankListSerializer(serializers.ModelSerializer):
    
    bank_combinations = BankCombinationsSerializer(many=True,read_only=True)

    class Meta:
        model = Bank
        fields = "__all__"

    

class BankSerializer(serializers.ModelSerializer):
    
    bank_combinations = BankCombinationsSerializer(many=True,read_only=True)

    class Meta:
        model = Bank
        fields = "__all__"

    def to_representation(self,obj):
        
        if self.context.get('search'):
            search_word = self.context.get('search')
            ret = super().to_representation(obj)
            challenge_list = BankCombinations.objects.filter(Q(bank_id=obj.id) & (Q(solution__icontains=search_word) | Q(challenge__name__icontains=search_word) )).values_list('challenge_id',flat=True).distinct()
            combinations_list = BankCombinations.objects.filter(Q(bank_id=obj.id) & Q(challenge__in=challenge_list))
            ret['bank_combinations'] = BankCombinationsSerializer(combinations_list,many=True).data
            ret['logo'] = 'https://brokeriq.com.au' + f'{obj.logo.url}'
            return ret
        else:
            res = super().to_representation(obj)
            res['logo'] = 'https://brokeriq.com.au' + f'{obj.logo.url}'
            return res


class BankImageSerializer(serializers.Serializer):

    id = serializers.IntegerField()
    image = serializers.ImageField(validators=[FileExtensionValidator(allowed_extensions=['jpg','jpeg','png'])])


    def validate(self, attrs):

        id = attrs.get('id')

        try:
            Bank.objects.get(id=id)
        except:
            raise exceptions.ValidationError({'detail':'Bank not found,try again'})       

        return attrs