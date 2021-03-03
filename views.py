from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.views import APIView
from django.contrib.auth.models import User, Group
from .models import FAQ, Instruction, VSMProfile
from .models import  CompanyCMPRecord, Company, Holding, Transaction
from .serializers import FAQSerializer, InstructionSerializer, VSMProfileSerializer
from .serializers import CompanySerializer, CmpSerializer, HoldingSerializer, TransactionSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from rest_framework.response import Response
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from django.http import HttpResponse
from rest_framework.decorators import api_view
from ca_dashboard.serializers import UserSerializer
from .serializers import AccessTokenSerializer
from oauth2_provider.models import AccessToken

import logging

logger = logging.getLogger(__name__)

class ACTViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = AccessToken.objects.all()
    serializer_class = AccessTokenSerializer
    permission_classes = [AllowAny]

class FaqViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = FAQ.objects.all()
    serializer_class = FAQSerializer
    permission_classes = [AllowAny]

class InstructionViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Instruction.objects.all()
    serializer_class = InstructionSerializer
    permission_classes = [AllowAny]

class CompanyViewSet(viewsets.ModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    permission_classes = [AllowAny]

class HoldingViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Holding.objects.all()
    serializer_class = HoldingSerializer
    permission_classes = [IsAdminUser]


@api_view(['GET'])
def my_holdings(request):
    profile = request.user.vsm_profile
    holdings = Holding.objects.filter(user=profile)
    holding_serializer = HoldingSerializer(holdings, many=True, context={'request': request})

    return Response(holding_serializer.data)

@api_view(['GET'])
def get_cmp_record(request):
    company = Company.objects.filter(code='googl')
    holdings = CmpSerializer.objects.filter()
    holding_serializer = CmpSerializer(holdings, many=True, context={'request': request})

    return Response(serializer.data)

@api_view(['POST', 'GET'])
def make_transaction(request):

    user = request.user
    if request.method == 'GET':
        profile_serializer = VSMProfileSerializer(request.user.vsm_profile, context={'request': request})

        transactions = Transaction.objects.filter(user=user.vsm_profile)[:100]
        transaction_serializer = TransactionSerializer(transactions, many=True, context={'request': request})

        return Response(transaction_serializer.data)
    elif request.method == 'POST':
        quant = int(request.POST['quantity'])
        transac_type = request.POST['transac_type']
        code = request.POST['code']
        company = Company.objects.get(code=code)
        user = request.user
        price = company.current_market_price
        transac = Transaction.objects.create(user=user.vsm_profile, company=company, transaction_type=transac_type, quantity= quant, bid_price=price)
        transac.save()
        
        transaction_serializer = TransactionSerializer(transac, context={'request': request})

        return Response(transaction_serializer.data)


@api_view(['GET', 'PATCH'])
def current_user(request):
    logger.info('current user')
    if request.method == 'GET':
        profile_serializer = VSMProfileSerializer(request.user.vsm_profile, context={'request': request})
        return Response(profile_serializer.data)
    
    elif request.method == 'PATCH':
        profile_serializer = VSMProfileSerializer(request.user.vsm_profile,data=request.data, partial=True, context={'request': request})
        profile_serializer.is_valid(raise_exception=True)
        profile_serializer.save()
        return Response(profile_serializer.data)


class LeaderViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = VSMProfile.objects.all().order_by('-cash')[:50]
    serializer_class = VSMProfileSerializer
    permission_classes = []

class IITBLViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = VSMProfile.objects.all().filter(is_iitb=True).order_by('-cash')[:10]
    serializer_class = VSMProfileSerializer
    permission_classes = []



class VSMProfileViewSet(viewsets.ModelViewSet):
    queryset = VSMProfile.objects.all()
    serializer_class = VSMProfileSerializer
    permission_classes = [IsAuthenticated]

    def list(self, request):
        if "sudhanshu" in self.request.user.username:
            return super().list(request)
        else:
            return Response({"status": "deny"})
    
    
    def create(self, request):
        return Response({"message": "not allowed on this path"})

    def retrieve(self, request, pk=None):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        if self.request.user.username == serializer.data['username']:
            return Response(serializer.data)
        else:
            return Response({"access": "deny"})

    
    def update(self, request, pk=None):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        if self.request.user.username == serializer.data['username']:
            return super().update(request, pk)
        elif self.request.user.username == 'sudhanshusahil':
            return super().update(request, pk)
        else:
            return Response({"access": "deny"})
            

    def partial_update(self, request, pk=None, *args, **kwargs):
        print("partial me aaya na")
        # kwargs['partial'] = True
        instance = self.get_object()
        serializer = self.get_serializer(instance, data = request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        if self.request.user.username == serializer.data['username']:
            return Response(serializer.data)
        elif self.request.user.username == 'sudhanshusahil':
            return Response(serializer.data)
        else:
            return Response({"access": "deny"})

    

    def destroy(self, request, pk=None):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        if self.request.user.username == serializer.data['username']:
            return super().destroy(request, pk)
        elif self.request.user.username == 'sudhanshusahil':
            return super().destroy(request, pk)
        else:
            return Response({"access": "deny"})
            