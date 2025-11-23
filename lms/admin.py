from django.contrib import admin

# Register your models here.
from .models import Course, Lesson, Enrollment, Review

admin.site.register(Course)
admin.site.register(Lesson)
admin.site.register(Enrollment)
admin.site.register(Review)