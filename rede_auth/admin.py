from django.contrib import admin

from rede_auth.models import Student, Teacher, User

# Register your models here.
class UserAdmin(admin.ModelAdmin):
    list_display = (
        'email',
    )

class StudentAdmin(admin.ModelAdmin):
    list_display = (
        'email',
    )

class TeacherAdmin(admin.ModelAdmin):
    list_display = (
        'email',
    )

admin.site.register(User, UserAdmin)
admin.site.register(Student, UserAdmin)
admin.site.register(Teacher, UserAdmin)