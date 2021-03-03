from django.contrib.auth.models import User, Group
from rest_framework import serializers
from .models import FAQ, Instruction, VSMProfile
from .models import  CompanyCMPRecord, Company, Holding, Transaction
from rest_framework.authtoken.models import Token
from oauth2_provider.models import AccessToken

class AccessTokenSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    email = serializers.CharField(source='user.email', read_only=True)
    fname = serializers.CharField(source="user.first_name", read_only=True)
    lname = serializers.CharField(source="user.last_name", read_only=True)
    class Meta:
        model = AccessToken
        fields = '__all__'

class VSMProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    email = serializers.CharField(source='user.email', read_only=True)
    fname = serializers.CharField(source="user.first_name", read_only=True)
    lname = serializers.CharField(source="user.last_name", read_only=True)
    class Meta:
        model = VSMProfile
        fields = '__all__'


class FAQSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = FAQ
        fields = '__all__'

class InstructionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Instruction
        fields = '__all__'

class CompanySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Company
        fields = '__all__'

class CmpSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompanyCMPRecord
        fields = '__all__'

class TransactionSerializer(serializers.ModelSerializer):
    company_name = serializers.CharField(source='company.name', read_only=True)
    company_code = serializers.CharField(source='company.code', read_only=True)
    company_cmp = serializers.CharField(source='company.current_market_price', read_only=True)
    username = serializers.CharField(source='user.user.username', read_only=True)
    class Meta:
        model = Transaction
        fields = '__all__'

class HoldingSerializer(serializers.ModelSerializer):
    company_name = serializers.CharField(source='company.name', read_only=True)
    company_code = serializers.CharField(source='company.code', read_only=True)
    company_cmp = serializers.CharField(source='company.current_market_price', read_only=True)
    username = serializers.CharField(source='user.user.username', read_only=True)
    class Meta:
        model = Holding
        fields = '__all__'
