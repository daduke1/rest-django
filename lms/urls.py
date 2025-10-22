# lms/urls.py
from rest_framework.routers import DefaultRouter
from .views import CourseViewSet, LessonViewSet, EnrollmentViewSet, CommentViewSet

router = DefaultRouter()
router.register(r"courses", CourseViewSet)
router.register(r"lessons", LessonViewSet)
router.register(r"enrollments", EnrollmentViewSet)
router.register(r"comments", CommentViewSet)

urlpatterns = router.urls
