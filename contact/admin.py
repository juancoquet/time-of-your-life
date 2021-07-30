from django.contrib import admin

from .models import Feedback


class FeedbackAdmin(admin.ModelAdmin):
    list_display = ['subject', 'short_msg', 'email', 'user']


admin.site.register(Feedback, FeedbackAdmin)
