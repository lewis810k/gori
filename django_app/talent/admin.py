from django.contrib import admin

from talent.models import Location, Talent, ClassImage, Registration, WishList, Curriculum, Review


class LocationInline(admin.TabularInline):
    model = Location


class CurriculumInline(admin.TabularInline):
    model = Curriculum


class ClassImageInline(admin.TabularInline):
    model = ClassImage


class RegistrationInline(admin.TabularInline):
    model = Registration


class TalentAdmin(admin.ModelAdmin):
    list_display = ('title', 'location', 'tutor', 'students_list')
    inlines = [LocationInline, ClassImageInline, CurriculumInline,]

    def tutor(self, talent):
        return talent.tutor

    def students_list(self, talent):
        student_list = []
        for student in talent.locations.values_list('registered_student', flat=True):
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
admin.site.register(Review)
