from django.contrib import admin
from django.contrib.admin import AllValuesFieldListFilter
from django_admin_listfilter_dropdown.filters import DropdownFilter

from member.models import GoriUser, Tutor
from talent.admin import RegistrationInline


class CustomDropdownFilter(AllValuesFieldListFilter):
    template = 'admin/dropdown_filter.html'


class TutorInline(admin.TabularInline):
    model = Tutor


class GoriUserAdmin(admin.ModelAdmin):
    list_display = ('pk', 'username', 'email', 'is_staff', 'is_active',
                    'joined_date', 'is_tutor', 'get_tutor_info',)
    inlines = [TutorInline, RegistrationInline]
    list_display_links = list_display

    list_filter = (
        ('is_tutor', DropdownFilter),
        ('is_staff', DropdownFilter),
    )

    def get_tutor_info(self, user):
        return user.tutor


class TutorAdmin(admin.ModelAdmin):
    list_display = ('pk', 'user', 'talent_count',)
    list_display_links = list_display

    def talent_count(self, obj):
        return obj.talent_set.count()

    def talent_title(self, tutor):
        title_list = []
        for index, item in enumerate(tutor.talent_set.values_list('title', flat=True)):
            title_list.append('{}:{}'.format(index + 1, item))
        return title_list


admin.site.register(GoriUser, GoriUserAdmin)
admin.site.register(Tutor, TutorAdmin)
