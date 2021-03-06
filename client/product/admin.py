from django.contrib import admin
from .models import ProductQue


class QueAdmin(admin.ModelAdmin):
    list_display = ("pk", "date", "is_resolved", "status")
    list_display_links = ("pk", )


admin.site.register(ProductQue, QueAdmin)
