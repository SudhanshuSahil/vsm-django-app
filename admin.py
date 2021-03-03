from django.contrib import admin
from vsm import models
from .models import VSMProfile, FAQ, Instruction
from organizations.models import Organization, OrganizationUser, OrganizationOwner

class VSMProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'demat_accout', 'cash', 'is_iitb',)
    list_filter = ()
    search_fields = ['user__username', 'user__first_name', 'user__last_name', 'roll_number', 'cash', 'is_iitb',]

# Register your models here.
admin.site.register(VSMProfile, VSMProfileAdmin)
admin.site.register(FAQ)
admin.site.register(Instruction)
admin.site.register(models.News)

class CompanyAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'current_market_price', 'change', 'stocks_availible')
    list_filter = ()
    search_fields = ['name', 'code', ]


admin.site.register(models.Company, CompanyAdmin)

class TransactionAdmin(admin.ModelAdmin):
    list_display = ('user', 'company', 'quantity', 'transaction_type', 'bid_price', 'verified')
    list_filter = ('verified', )
    readonly_fields = ['verified', ]
    search_fields = ['company', 'user', 'quantity',]

admin.site.register(models.Transaction, TransactionAdmin)

class HoldingAdmin(admin.ModelAdmin):
    list_display = ('company', 'user', 'quantity',)
    list_filter = ()
    search_fields = ['company', 'user',]

admin.site.register(models.Holding, HoldingAdmin)


class CmpAdmin(admin.ModelAdmin):
    list_display = ('company', 'cmp', 'change', 'timestamp')
    list_filter = ('company', 'timestamp')
    search_fields = ['company', 'cmp', 'timestamp',]


admin.site.register(models.CompanyCMPRecord, CmpAdmin)

admin.site.unregister(Organization)
admin.site.unregister(OrganizationUser)
admin.site.unregister(OrganizationOwner)
