from django.contrib import admin

from member.models import GoriUser
from talent.models import Location, Talent, ClassImage, Registration


class TalentAdmin(admin.ModelAdmin):
    list_display = ('class_title', 'location', 'tutor', 'students_list',)

    def tutor(self, talent):
        return talent.tutor

    def students_list(self, talent):
        student_list = []
        for student_id in talent.registration_set.values_list('student_id', flat=True):
            student_list.append(GoriUser.objects.get(id=student_id))
        return student_list

    def location(self, talent):
        location_list = []
        for location in talent.location_set.values_list('region', flat=True):
            location_list.append(location)
        return location_list


admin.site.register(Location)
admin.site.register(Talent, TalentAdmin)
admin.site.register(ClassImage)
admin.site.register(Registration)
