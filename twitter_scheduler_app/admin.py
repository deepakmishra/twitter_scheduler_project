from django.contrib import admin
from django.contrib.auth.models import User
from django.db import models
from django.forms import TextInput, Textarea
from twitter_scheduler_app.models import Credential, Post, PostStatus

@admin.register(Credential)
class CredentialAdmin(admin.ModelAdmin):

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "user":
            kwargs["initial"] = request.user.id
            if not request.user.is_superuser:
                kwargs["disabled"] = True
        return super(CredentialAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

    def get_queryset(self, request):
        qs = super(CredentialAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(user=request.user)


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):

    list_filter = ["status"]
    readonly_fields = ["twitter_response"]
    list_display = ["content_ellipsis", "parent", "status", "schedule", "sent_at", "hours_from_parent", "hours_from_now"]

    def content_ellipsis(self, obj):
        if len(obj.content) > 100:
            return "%s..." % obj.content[:100]
        return obj.content

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "user":
            kwargs["initial"] = request.user.id
            kwargs["disabled"] = True
        elif db_field.name == "parent":
            kwargs["queryset"] = request.user.posts

        return super(PostAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        form.base_fields["status"].widget.choices = [(PostStatus.SCHEDULED.value, PostStatus.SCHEDULED.name)]
        return form

    def get_queryset(self, request):
        qs = super(PostAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(user=request.user)
