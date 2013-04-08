__author__ = 'Brandon'
from django.contrib import admin
from banking import models as banking_models


class AccountAdmin(admin.ModelAdmin):
    exclude = ('balance',)

class CheckingAdmin(admin.ModelAdmin):
    exclude = ('balance',)


class SavingAdmin(admin.ModelAdmin):
    exclude = ('balance',)

admin.site.register(banking_models.Account,AccountAdmin)
admin.site.register(banking_models.Checking,CheckingAdmin)
admin.site.register(banking_models.Saving,SavingAdmin)
admin.site.register(banking_models.Check)
admin.site.register(banking_models.Expense)
admin.site.register(banking_models.Payee)
