# lms/views.py
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from .models import Course, Lesson, Enrollment, Comment
from .serializers import CourseSerializer, LessonSerializer, EnrollmentSerializer, CommentSerializer
from django.shortcuts import render

def index(request):
    return render(request, 'index.html')

class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.select_related("instructor").all()
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filterset_fields = ["instructor"]
    search_fields = ["title", "description"]
    ordering_fields = ["created_at", "updated_at"]
    ordering = ["-created_at"]

    def perform_create(self, serializer):
        if "instructor" not in serializer.validated_data:
            serializer.save(instructor=self.request.user)
        else:
            serializer.save()

class LessonViewSet(viewsets.ModelViewSet):
    queryset = Lesson.objects.select_related("course").all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filterset_fields = ["course"]
    search_fields = ["title", "content"]
    ordering_fields = ["order", "created_at"]
    ordering = ["order"]

class EnrollmentViewSet(viewsets.ModelViewSet):
    queryset = Enrollment.objects.select_related("user", "course").all()
    serializer_class = EnrollmentSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        if "user" not in serializer.validated_data:
            serializer.save(user=self.request.user)
        else:
            serializer.save()

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.select_related("user", "course").all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filterset_fields = ["course", "user"]
    ordering_fields = ["published_at"]
    ordering = ["-published_at"]
