# lms/views.py
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from .models import Course, Lesson, Enrollment, Review
from .serializers import CourseSerializer, LessonSerializer, EnrollmentSerializer, ReviewSerializer
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse, Http404
from django.contrib import messages
from django.contrib.auth.decorators import login_required

def index(request):
    courses = Course.objects.all()
    context = {
        'courses': courses
    }
    return render(request, 'index.html', context)

def course_detail(request, slug):
    """
    View to display complete course information including:
    - Course details (title, description, instructor, price, etc.)
    - Lessons list
    - Reviews and ratings
    - Enrollment status (if user is authenticated)
    """
    course = get_object_or_404(
        Course.objects.select_related('instructor').prefetch_related('lessons', 'reviews__user'),
        slug=slug
    )
    
    # Get lessons ordered by order field
    lessons = course.lessons.all().order_by('order', 'id')
    
    # Get reviews with user information
    reviews = course.reviews.all().select_related('user')
    
    # Calculate average rating
    if reviews.exists():
        avg_rating = sum(review.rating for review in reviews) / reviews.count()
        avg_rating = round(avg_rating, 1)
    else:
        avg_rating = None
    
    # Check if user is enrolled (if authenticated)
    is_enrolled = False
    enrollment = None
    is_instructor = False
    if request.user.is_authenticated:
        is_instructor = (request.user == course.instructor)
        try:
            enrollment = Enrollment.objects.get(user=request.user, course=course)
            is_enrolled = True
        except Enrollment.DoesNotExist:
            pass
    
    # Calculate total course duration
    total_duration = sum(lesson.duration_minutes for lesson in lessons)
    
    # Get enrollment count
    enrollment_count = course.enrollments.count()
    
    context = {
        'course': course,
        'lessons': lessons,
        'reviews': reviews,
        'avg_rating': avg_rating,
        'total_reviews': reviews.count(),
        'is_enrolled': is_enrolled,
        'enrollment': enrollment,
        'is_instructor': is_instructor,
        'total_duration': total_duration,
        'enrollment_count': enrollment_count,
    }
    
    return render(request, 'course_detail.html', context)

@login_required
def enroll_course(request, slug):
    """
    View to handle course enrollment.
    Only authenticated users can enroll.
    """
    if request.method != 'POST':
        messages.error(request, 'Método no permitido.')
        return redirect('course_detail', slug=slug)
    
    course = get_object_or_404(Course, slug=slug)
    
    # Prevent instructor from enrolling in their own course
    if request.user == course.instructor:
        messages.warning(request, 'No puedes inscribirte en tu propio curso.')
        return redirect('course_detail', slug=slug)
    
    # Check if user is already enrolled
    enrollment, created = Enrollment.objects.get_or_create(
        user=request.user,
        course=course
    )
    
    if created:
        messages.success(request, f'¡Te has inscrito exitosamente en "{course.title}"!')
    else:
        messages.info(request, f'Ya estás inscrito en "{course.title}".')
    
    return redirect('course_detail', slug=slug)

@login_required
def my_courses(request):
    """
    View to display all courses the logged-in user is enrolled in.
    Shows enrollment date, completion status, and course details.
    """
    enrollments = Enrollment.objects.filter(
        user=request.user
    ).select_related('course', 'course__instructor').prefetch_related('course__lessons').order_by('-enrolled_at')
    
    # Calculate stats for each enrollment
    courses_data = []
    for enrollment in enrollments:
        course = enrollment.course
        lessons = course.lessons.all()
        total_lessons = lessons.count()
        total_duration = sum(lesson.duration_minutes for lesson in lessons)
        
        courses_data.append({
            'enrollment': enrollment,
            'course': course,
            'total_lessons': total_lessons,
            'total_duration': total_duration,
            'enrollment_count': course.enrollments.count(),
        })
    
    context = {
        'courses_data': courses_data,
        'total_enrolled': len(courses_data),
    }
    
    return render(request, 'my_courses.html', context)

def registro(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.is_active = False
            user.save()
            messages.success(
                request, 'Registro exitoso, revisa tu correo para activar.')
            return redirect('login')
    else:
        form = RegistroForm()
    return render(request, 'usuarios/registro.html', {'form': form})

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

class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.select_related("user", "course").all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filterset_fields = ["course", "user"]
    ordering_fields = ["published_at"]
    ordering = ["-published_at"]

def list_courses_ajax(request):
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest' and request.method == 'GET':
        courses = list(Course.objects.all().values(
            'id', 'title', 'description'))
        return JsonResponse({'courses': courses})
    return JsonResponse({'error': 'bad request'}, status=400)