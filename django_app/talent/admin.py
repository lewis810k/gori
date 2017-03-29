from django.contrib import admin

from talent.models import Location, Talent, ClassImage, Registration, WishList, Curriculum


class LocationInline(admin.TabularInline):
    model = Location


class RegistrationInline(admin.TabularInline):
    model = Registration


class TalentAdmin(admin.ModelAdmin):
    list_display = ('class_title', 'location', 'tutor', 'students_list')
    inlines = [LocationInline, ]

    def tutor(self, talent):
        return talent.tutor

    def students_list(self, talent):
        student_list = []
        for student in talent.location_set.values_list('registered_student', flat=True):
            student_list.append(student)
        return student_list

    def location(self, talent):
        location_list = []
        for location in Location.objects.filter(talent=talent):
            location_list.append(location.get_region_display())
        return location_list


class LocationAdmin(admin.ModelAdmin):
    list_display = ['get_region_display']
    inlines = [RegistrationInline, ]


admin.site.register(Location, LocationAdmin)
admin.site.register(Talent, TalentAdmin)
admin.site.register(ClassImage)
admin.site.register(Registration)
admin.site.register(WishList)
admin.site.register(Curriculum)
