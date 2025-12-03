# lms/models.py
from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify

class Course(models.Model):
    title = models.CharField(max_length=200)
    # Slug único para URLs amigables (ej: /curso/aprende-django/)
    slug = models.SlugField(unique=True, blank=True) 
    
    # Diferencia entre resumen corto (para cards) y descripción completa
    short_description = models.CharField(max_length=150, blank=True) 
    description = models.TextField(blank=True)
    
    instructor = models.ForeignKey(User, on_delete=models.CASCADE, related_name="courses_taught")
    
    # Imagen de portada (requiere instalar Pillow: pip install Pillow)
    thumbnail = models.ImageField(upload_to='courses/thumbnails/', blank=True, null=True)
    
    # Precio (Decimal es mejor que Float para dinero)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    
    # Control de visibilidad
    is_published = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)


class Lesson(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="lessons")
    title = models.CharField(max_length=200)
    content = models.TextField(blank=True) # El texto puede ser opcional si es solo video
    
    # Soporte para video (URL externa o ID de video)
    video_url = models.URLField(blank=True, null=True)
    
    # Duración estimada en minutos
    duration_minutes = models.PositiveIntegerField(default=0)
    
    order = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["order", "id"]
        unique_together = [("course", "order")]

    def __str__(self):
        return f"{self.course.title} - {self.title}"


class Enrollment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="enrollments")
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="enrollments")
    enrolled_at = models.DateTimeField(auto_now_add=True)
    
    # Progreso
    is_completed = models.BooleanField(default=False)

    class Meta:
        unique_together = [("user", "course")]

    def __str__(self):
        return f"{self.user.username} -> {self.course.title}"


class Review(models.Model): # Renombrado de Comment a Review para ser más preciso
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="reviews")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reviews")
    comment = models.TextField()
    
    # Calificación de 1 a 5 estrellas
    rating = models.PositiveIntegerField(choices=[(i, i) for i in range(1, 6)], default=5)
    
    published_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-published_at"]
        # Evita que un usuario califique el mismo curso dos veces
        unique_together = [("user", "course")] 

    def __str__(self):
        return f"{self.rating} stars - {self.user.username} on {self.course.title}"