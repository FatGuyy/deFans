from django.contrib import admin
from .models import Creator, Account, CreatorPost

# Register your models here.
class AuthorAdmin(admin.ModelAdmin):
    pass

admin.site.register(Creator, AuthorAdmin)
admin.site.register(Account, AuthorAdmin)
admin.site.register(CreatorPost, AuthorAdmin)