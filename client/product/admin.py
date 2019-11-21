from django.contrib import admin
from .models import ProductQue


class QueAdmin(admin.ModelAdmin):
    list_display = ("date", "is_resolved", "status")


admin.site.register(ProductQue, QueAdmin)
