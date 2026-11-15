from django.contrib import admin
from .models import *



@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('name', 'roll_no')



@admin.register(TextDemo)
class TextDemoAdmin(admin.ModelAdmin):
    list_display = ("char", "slug", "email", "status", "uid")
    search_fields = ("char", "email")
    list_filter = ("status",)
    prepopulated_fields = {"slug": ("char",)}
    readonly_fields = ("uid",)


@admin.register(NumberDemo)
class NumberDemoAdmin(admin.ModelAdmin):
    list_display = ("id", "integer", "float_num", "decimal_num", "rating")
    list_filter = ("rating",)


@admin.register(DateTimeDemo)
class DateTimeDemoAdmin(admin.ModelAdmin):
    list_display = ("id", "date", "time", "datetime", "duration", "created_at")
    date_hierarchy = "date"
    readonly_fields = ("created_at", "updated_at")


@admin.register(FileDemo)
class FileDemoAdmin(admin.ModelAdmin):
    list_display = ("title", "file", "image", "py_file")
    search_fields = ("title",)


@admin.register(MiscDemo)
class MiscDemoAdmin(admin.ModelAdmin):
    list_display = ("id", "is_active", "is_verified", "price", "qty", "total")
    list_filter = ("is_active", "is_verified")
    readonly_fields = ("total",)


class LabBookInline(admin.TabularInline):
    model = LabBook
    extra = 1


@admin.register(LabAuthor)
class LabAuthorAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)
    inlines = [LabBookInline]


@admin.register(LabBook)
class LabBookAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "editor")
    list_filter = ("author",)
    search_fields = ("title",)
    raw_id_fields = ("editor",)


@admin.register(LabProfile)
class LabProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "bio")


@admin.register(LabCourse)
class LabCourseAdmin(admin.ModelAdmin):
    list_display = ("name",)


@admin.register(LabStudent)
class LabStudentAdmin(admin.ModelAdmin):
    list_display = ("name",)
    filter_horizontal = ("courses",)    


