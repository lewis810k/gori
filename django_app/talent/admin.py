from django.contrib import admin

from talent.models import Review, Location, Talent, ClassImage, Registration, WishList, Curriculum


class LocationInline(admin.TabularInline):
    model = Location


class CurriculumInline(admin.TabularInline):
    model = Curriculum


class ClassImageInline(admin.TabularInline):
    model = ClassImage


class RegistrationInline(admin.TabularInline):
    model = Registration


class RegistrationAdmin(admin.ModelAdmin):
    list_display = ('student_name',
                    'title',
                    'location',
                    'joined_date',
                    'is_confirmed',
                    'student_level',
                    'experience_length',)
    list_filter = ('student', 'talent_location')

    def student_name(self, registration):
        return registration.student.name

    student_name.short_description = 'student'

    def location(self, registration):
        return registration.talent_location.get_region_display()

    def title(self, registration):
        return registration.talent_location.talent.title


class CurriculumAdmin(admin.ModelAdmin):
    list_display = ('pk', 'talent_title', 'tutor')
    list_filter = ('talent',)

    def talent_title(self, curriculum):
        return curriculum.talent.title

    talent_title.short_description = 'title'

    def tutor(self, curriculum):
        return curriculum.talent.tutor.user.name


class ClassImageAdmin(admin.ModelAdmin):
    list_display = ('pk', 'talent', 'tutor', 'image',)
    list_filter = ('talent',)
    ordering = ('talent',)

    def talent(self, classimage):
        return classimage.talent.title

    def tutor(self, classimage):
        return classimage.talent.tutor.user.name


class TalentAdmin(admin.ModelAdmin):
    list_display = ('title', 'location', 'tutor', 'students_list')
    inlines = [LocationInline, ClassImageInline, CurriculumInline, ]

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
    list_display = ('pk', 'talent', 'registered_students')
    inlines = [RegistrationInline, ]

    def talent(self, location):
        return location.talent.title

    def registered_students(self, location):
        return [registrations.student.name for registrations in Registration.objects.filter(talent_location=location)]
        # for registrations in Registration.objects.filter(talent_location=location):
        #     student.append(registrations.student)
        # return student


admin.site.register(Location, LocationAdmin)
admin.site.register(Talent, TalentAdmin)
admin.site.register(ClassImage, ClassImageAdmin)
admin.site.register(Registration, RegistrationAdmin)
admin.site.register(WishList)
admin.site.register(Curriculum, CurriculumAdmin)
admin.site.register(Review)
