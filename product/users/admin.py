from django.contrib import admin
from .models import Balance


class BalanceAdmin(admin.ModelAdmin):
    list_display = ('user', 'amount')


admin.site.register(Balance, BalanceAdmin)
