from django.contrib import admin

# Register your models here.
from talent.models import Location, Talent, ClassImage, Registration

admin.site.register(Location)
admin.site.register(Talent)
admin.site.register(ClassImage)
admin.site.register(Registration)