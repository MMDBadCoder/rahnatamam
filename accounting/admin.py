from django.contrib import admin

# Register your models here.
from accounting.models import Account, Human


@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    pass


@admin.register(Human)
class HumanAdmin(admin.ModelAdmin):
    pass
