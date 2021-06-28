from django.contrib import admin
from .models import *


class BankCombinationInline(admin.TabularInline):
    model = BankCombinations
    extra = 3


class SolutionInline(admin.TabularInline):
    model = Solution
    extra = 2


class ChallangeAdmin(admin.ModelAdmin):
    list_display = ['id','name']
    # inlines = [SolutionInline]

admin.site.register(Challenge,ChallangeAdmin)

class SolutionAdmin(admin.ModelAdmin):
    list_display = ['id','name']

admin.site.register(Solution,SolutionAdmin)


class BankAdmin(admin.ModelAdmin):

    inlines = [BankCombinationInline]

admin.site.register(Bank,BankAdmin)
