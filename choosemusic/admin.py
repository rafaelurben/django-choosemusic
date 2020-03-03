from django.contrib import admin, messages
from django.contrib.auth.models import User, Group, Permission
from .models import Einreichung

# Register your models here.

class EinreichungenAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Song', {'fields': ['link']}),
        ('Status', {'fields': ['status']}),
    ]
    list_display = ('titel', 'kuenstler', 'link', 'benutzer', 'status', 'timestamp')
    list_filter = ['timestamp']
    search_fields = ['titel','kuenstler','benutzer']

    actions = ["play_again","allow","disallow"]

    verbose_name = "Frage"
    verbose_name_plural = "Fragen"

    def get_actions(self, request):
            actions = super(EinreichungenAdmin, self).get_actions(request)
            if not request.user.has_perm("change_einreichung"):
               del actions["play_again"]
               del actions["allow"]
               del actions["disallow"]
            return actions

    def get_form(self, request, obj=None, **kwargs):
        form = super(EinreichungenAdmin, self).get_form(request, obj, **kwargs)
        if request.user.has_perm("change_einreichung"):
            form.base_fields['status'].choices = (('playlist', 'In der Playlist'),('wait', 'Auf Überprüfung warten...'),('forbidden', 'Wurde nicht zugelassen'))
        return form

    def save_model(self, request, instance, form, change):
        user = request.user
        instance = form.save(commit=False)
        instance.benutzer = user
        instance.save()
        form.save_m2m()
        return instance

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ["link"]
        else:
            return []


    def play_again(self, request, queryset):
        rows_updated = queryset.filter(status="passed").update(status='playlist')
        if rows_updated == 0:
            self.message_user(request, "Keine Einreichungen werden nochmals gespielt!", level=messages.constants.WARNING)
        elif rows_updated == 1:
            self.message_user(request, "Eine Einreichung wird nochmals gespielt!")
        else:
            self.message_user(request, "%s Einreichungen werden nochmals gespielt!" % rows_updated)
    play_again.short_description = "Nochmals abspielen"

    def allow(self, request, queryset):
        rows_updated = queryset.filter(status="wait").update(status='playlist')
        if rows_updated == 0:
            self.message_user(request, "Keine Einreichungen wurden der Playlist hinzugefügt!", level=messages.constants.WARNING)
        elif rows_updated == 1:
            self.message_user(request, "EIne Einreichung wurde der Playlist hinzugefügt!")
        else:
            self.message_user(request, "%s Einreichungen wurden der Playlist hinzugefügt!" % rows_updated)
    allow.short_description = "Erlauben und zur Playlist hinzufügen"

    def disallow(self, request, queryset):
        rows_updated = queryset.filter(status="wait").update(status='forbidden')
        if rows_updated == 0:
            self.message_user(request, "Keine Einreichungen wurden verboten!", level=messages.constants.WARNING)
        elif rows_updated == 1:
            self.message_user(request, "EIne Einreichung wurde verboten!")
        else:
            self.message_user(request, "%s Einreichungen wurden verboten!" % rows_updated)
    disallow.short_description = "Verbieten"


admin.site.register(Einreichung, EinreichungenAdmin)
