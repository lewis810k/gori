from django.contrib import admin

# Register your models here.
from member.models import GoriUser, Tutor

admin.site.register(GoriUser)
admin.site.register(Tutor)