from django.contrib import admin
from .models import Clients,ClientHistory

class ClientHistoryTab(admin.TabularInline):
    model = ClientHistory
    extra = 0

class ClientsAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Clients._meta.fields]
    inlines = [ClientHistoryTab]
    
admin.site.register(Clients,ClientsAdmin)
admin.site.register(ClientHistory)
