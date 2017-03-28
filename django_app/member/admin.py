from django.contrib import admin

from member.models import GoriUser, Tutor


class GoriUserAdmin(admin.ModelAdmin):
    list_display = ('email', 'is_staff', 'is_active',
                    'joined_date', 'is_tutor', 'get_tutor_info',)

    def get_tutor_info(self, user):
        return user.tutor


class TutorAdmin(admin.ModelAdmin):
    list_display = ('user', 'talent_title',)

    def talent_title(self, tutor):
        title_list = []
        for index, item in enumerate(tutor.talent_set.values_list('class_title', flat=True)):
            title_list.append('{}:{}'.format(index+1, item))
        return title_list


admin.site.register(GoriUser, GoriUserAdmin)
admin.site.register(Tutor, TutorAdmin)
