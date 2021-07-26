from django.contrib import admin

from .models import UserEvent


class UserEventAdmin(admin.ModelAdmin):
    list_display = ('event_name', 'owner', 'event_date',)


admin.site.register(UserEvent, UserEventAdmin)
