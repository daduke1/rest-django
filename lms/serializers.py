# lms/serializers.py
from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Course, Lesson, Enrollment, Review

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email", "first_name", "last_name"]

class CourseSerializer(serializers.ModelSerializer):
    instructor = UserSerializer(read_only=True)
    instructor_id = serializers.PrimaryKeyRelatedField(
        write_only=True, source="instructor", queryset=User.objects.all(), required=False
    )

    class Meta:
        model = Course
        fields = ["id", "title", "description", "instructor", "instructor_id", "created_at", "updated_at"]
        read_only_fields = ["id", "created_at", "updated_at", "instructor"]

class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = ["id", "course", "title", "content", "order", "created_at"]
        read_only_fields = ["id", "created_at"]

class EnrollmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Enrollment
        fields = ["id", "user", "course", "enrolled_at"]
        read_only_fields = ["id", "enrolled_at"]

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ["id", "course", "user", "comment", "rating", "published_at"]
        read_only_fields = ["id", "published_at"]
