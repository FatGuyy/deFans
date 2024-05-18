from django.contrib import admin
from django.utils.html import format_html
from .models import Creator, Account, CreatorPost, Subscription

# Register your models here.
class CreatorAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'short_bio', 'price')  # Display a shortened version of 'bio'

    def short_bio(self, obj):
        if len(obj.bio) > 50:
            return format_html(f"{obj.bio[:40]}...")
        return obj.bio

    short_bio.short_description = 'Bio'
    search_fields = ["nickName"]

class AccountAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'nickName', 'short_bio')
    
    def short_bio(self, obj):
        if len(obj.bio) > 50:
            return format_html(f"{obj.bio[:40]}...")
        return obj.bio

    short_bio.short_description = 'Bio'
    search_fields = ["nickName"]

class CreatorPostAdmin(admin.ModelAdmin):
    list_display = ["id", "uploader", "content"]
    search_fields = ["id", "uploader"]

admin.site.register(Creator, CreatorAdmin)
admin.site.register(Account, AccountAdmin)
admin.site.register(CreatorPost, CreatorPostAdmin)
admin.site.register(Subscription)