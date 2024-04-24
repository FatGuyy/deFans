from django.contrib import admin
from .models import Creator, Account, CreatorPost

# Register your models here.
class CreatorAdmin(admin.ModelAdmin):
    list_display = ["id", "nickName"]
    search_fields = ["nickName"]

class AccountAdmin(admin.ModelAdmin):
    list_display = ["id", "nickName"]
    search_fields = ["nickName"]

class CreatorPostAdmin(admin.ModelAdmin):
    list_display = ["id", "uploader"]
    search_fields = ["id", "uploader"]

admin.site.register(Creator, CreatorAdmin)
admin.site.register(Account, AccountAdmin)
admin.site.register(CreatorPost, CreatorPostAdmin)
