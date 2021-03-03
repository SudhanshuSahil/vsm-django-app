from django.db import models
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

from decimal import Decimal
import random
# Create your models here.

class VSMProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='vsm_profile')
    roll_number = models.TextField(max_length=250, blank=True, null=True)
    college = models.TextField(max_length=250, blank=True, null=True)
    is_iitb = models.BooleanField(blank=True, null=True)
    roll_number = models.CharField(default='not_iitb', max_length=10)
    program = models.TextField(max_length=250, blank=True, null=True)
    hostel = models.IntegerField(blank=True, null=True)
    cash = models.DecimalField(default=1000000, max_digits=50, decimal_places=10)
    city = models.TextField(max_length=250, blank=True, null=True)
    zip_code = models.TextField(max_length=250, blank=True, null=True)
    demat_accout = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.username}"
    
class CashRecord(models.Model):
    user = models.ForeignKey(VSMProfile, on_delete=models.CASCADE)
    cash = models.DecimalField(default=1000000, max_digits=50, decimal_places=10)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f'cash record of {self.user.user.username}'

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        VSMProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


class FAQ(models.Model):
    que = models.TextField()
    ans = models.TextField()

    def __str__(self):
        return f"Question : {self.que}"

class Instruction(models.Model):
    que = models.TextField(blank=True, null=True)
    ans = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Instruction : {self.que}"

class Company(models.Model):
    code = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=20, unique=True)
    market_cap = models.DecimalField(max_digits=20, decimal_places=2, default=0.00)
    current_market_price = models.DecimalField(max_digits=20, decimal_places=2, default=0.00)
    change = models.DecimalField(max_digits=10, decimal_places=2,default=0.00)
    stocks_availible = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.name} -- {self.code}'

    def get_cmp(self):
        return self.current_market_price

class News(models.Model):
    show_id = models.IntegerField(default=0)
    related_company = models.ManyToManyField(Company, blank=True)
    title = models.CharField(max_length=120)
    content = models.TextField()
    is_active = models.BooleanField(default=True)  # Inactive news won't appear in dashboard
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-timestamp', '-updated']

    def __str__(self):
        return self.title


TRANSACTION_MODES = (
    ('buy', 'BUY'),
    ('sell', 'SELL')
)

class Transaction(models.Model):
    user = models.ForeignKey(VSMProfile, on_delete=models.CASCADE)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    transaction_type = models.CharField(max_length=20, choices=TRANSACTION_MODES, blank=True, null=True)
    quantity = models.IntegerField(default=0)
    bid_price = models.DecimalField(default=0, decimal_places=4, max_digits=20)
    verified = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.company.name} -- {self.user} -- {self.quantity}'


class Holding(models.Model):
    user = models.ForeignKey(VSMProfile, on_delete=models.CASCADE)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)

    class Meta:
        unique_together = ('user', 'company',)

    def __str__(self):
        return f'{self.user} -- {self.company} -- {self.quantity}'


class CompanyCMPRecord(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    cmp = models.DecimalField(max_digits=20, decimal_places=2, default=0.00)
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    change = models.DecimalField(max_digits=10, decimal_places=2,default=0.00)

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return self.company.code


# @receiver(pre_save, sender=Company)
# def pre_add_company_reciever(sender, instance, *arg, **kwargs):
#     if instance.pk is not None:
#         old = Company.objects.filter(pk=instance.pk)
#         if old.count == 1:
#             change = instance.current_market_price - old.current_market_price
#             instance._change = change
#         else:
#             change = 0
#             instance._change = change

#         # record = CompanyCMPRecord(company=instance, cmp=instance.current_market_price, change=change)
#         # record.save()
    
#     else:
#         instance._change = 0

# @receiver(post_save, sender=Company)
# def add_company_reciever(sender, instance, *arg, **kwargs):
#     change1 = instance._change
#     Company.objects.filter(pk = instance.pk).update(change=change1)



@receiver(post_save, sender=Transaction)
def save_transaction(sender, instance, created, **kwargs):
    if created:
        print("bid", instance.bid_price)
        print("cmp", instance.company.current_market_price)
        print("typ", instance.transaction_type)
        quantity = instance.quantity
        bid = instance.bid_price
        cmp = instance.company.current_market_price
        user = instance.user
        cash = user.cash
        
        try:
            holding1 = Holding.objects.get(user=instance.user, company=instance.company)
            owned_shares = holding1.quantity
        except Exception:
            owned_shares = 0


        if instance.transaction_type == 'buy' and bid >= cmp and cash > bid*quantity:
            print ('Validated')
            Transaction.objects.filter(pk=instance.pk).update(verified=True)

            try:
                holding = Holding.objects.get(user=instance.user, company=instance.company)
            except Exception:
                holding = Holding.objects.create(user=instance.user, company=instance.company, quantity=0)
        
            holding.quantity += quantity
            holding.save()

            if instance.company.stocks_availible == 0:
                instance.company.stocks_availible = 1000
            
            instance.company.stocks_availible += quantity

            multiplier = Decimal(quantity) / Decimal(instance.company.stocks_availible)
            multiplier *= Decimal(random.uniform(0.5, 1.5))
            old = instance.company.current_market_price

            instance.company.current_market_price *=  multiplier+1

            instance.company.change = instance.company.current_market_price - old

            instance.company.save()
            count = Company.objects.count()
            print(count)
            for company in Company.objects.all():
                if company.stocks_availible == 0:
                    company.stocks_availible = 1000
                if company != instance.company:
                    multiplier = Decimal(quantity) / Decimal(company.stocks_availible)
                    multiplier *= Decimal(0.5)
                    old = company.current_market_price 
                    company.current_market_price *= ((multiplier * Decimal(random.uniform(-0.1, 0.1))) + 1)
                    company.change = company.current_market_price - old
                    company.save()

            user.cash -= bid*quantity
            user.save()
            
            

        elif instance.transaction_type == 'sell' and bid <= cmp and quantity <= owned_shares:
            print ('verified sellings')
            holding1.quantity -= quantity
            holding1.save()
            if holding1.quantity == 0:
                holding1.delete()

            user.cash += bid*quantity
            user.save()

            instance.company.stocks_availible -= quantity
            multiplier = Decimal(quantity) / Decimal(instance.company.stocks_availible)
            multiplier *= Decimal(random.uniform(0.5, 1.5))
            old = instance.company.current_market_price

            instance.company.current_market_price *=  1-multiplier

            instance.company.change = instance.company.current_market_price - old

            # instance.company.current_market_price *= Decimal(random.uniform(0.9, 1))
            instance.company.save()
            count = Company.objects.count()
            print(count)
            for company in Company.objects.all():
                if company.stocks_availible == 0:
                    company.stocks_availible = 1000
                if company != instance.company:
                    multiplier = Decimal(quantity) / Decimal(company.stocks_availible)
                    multiplier *= Decimal(0.5)
                    old = company.current_market_price 
                    company.current_market_price *= ((multiplier * Decimal(random.uniform(-0.1, 0.1))) + 1)
                    company.change = company.current_market_price - old
                    company.save()

            Transaction.objects.filter(pk=instance.pk).update(verified=True)

        else:
            print ("kahin nhi h")
    
    else:
        print("bid", instance.bid_price)
        print("cmp", instance.company.current_market_price)
        print("typ", instance.transaction_type)
        quantity = instance.quantity
        bid = instance.bid_price
        cmp = instance.company.current_market_price
        user = instance.user
        cash = user.cash
        
        try:
            holding1 = Holding.objects.get(user=instance.user, company=instance.company)
            owned_shares = holding1.quantity
        except Exception:
            owned_shares = 0

        if instance.transaction_type == 'buy' and bid >= cmp and cash > bid*quantity:
            print ('Validated')
            Transaction.objects.filter(pk=instance.pk).update(verified=True)
        
        elif instance.transaction_type == 'sell' and bid <= cmp and quantity <= owned_shares:
            print ('verified sellings')
            Transaction.objects.filter(pk=instance.pk).update(verified=True)
        else:
            print ('not f**in verified')



