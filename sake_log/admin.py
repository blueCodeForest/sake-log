from django.contrib import admin

from .models import DisplayAlcoholList, DrankAlcoholList, StatusList

admin.site.register(DisplayAlcoholList)
# admin.site.register(DrankAlcoholList)
admin.site.register(StatusList)

@admin.register(DrankAlcoholList)
class DrankAlcoholAdmin(admin.ModelAdmin):
    model = DrankAlcoholList
    list_display = ["drank_card", "user", "created_at"]