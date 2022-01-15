from django.contrib import admin

from .models import DisplayAlcoholList, AlcoholLogList, StatusList

admin.site.register(DisplayAlcoholList)
# admin.site.register(AlcoholLogList)
admin.site.register(StatusList)

@admin.register(AlcoholLogList)
class DrankAlcoholAdmin(admin.ModelAdmin):
    model = AlcoholLogList
    list_display = ["alcohol", "user", "created_at"]