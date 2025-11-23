# lms/urls.py
from rest_framework.routers import DefaultRouter
from .views import (
    CourseViewSet, 
    LessonViewSet, 
    EnrollmentViewSet, 
    ReviewViewSet,
    list_courses_ajax
)
from django.urls import path

router = DefaultRouter()
router.register(r"courses", CourseViewSet)
router.register(r"lessons", LessonViewSet)
router.register(r"enrollments", EnrollmentViewSet)
router.register(r"reviews", ReviewViewSet)

urlpatterns = router.urls

urlpatterns += [
    path('ajax/courses/', list_courses_ajax, name='list_courses_ajax'),
]