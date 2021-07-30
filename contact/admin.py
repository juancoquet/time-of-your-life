from django.contrib import admin

from .models import Feedback


class FeedbackAdmin(admin.ModelAdmin):
    list_display = ['short_msg', 'subject', 'email', 'user']


admin.site.register(Feedback, FeedbackAdmin)
