from django.contrib import admin
from rede_social.models import Profile

# Register your models here.


class ProfileAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'bio'
    )


admin.site.register(Profile, ProfileAdmin)
