from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):

    ROLE_CHOICES = (

        ('student', 'Student'),
        ('instructor', 'Instructor'),

    )

    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default='student'
    )

    profile_pic = models.ImageField(
        upload_to='profile_pics/',
        default='profile_pics/default.png'
    )

    def __str__(self):

        return self.username

# the course model

class Course(models.Model):

    COURSE_TYPES = (

        ('technology', 'Technology & Development'),

        ('career', 'Career & Professional Growth'),

        ('communication', 'Communication & Placement'),

        ('creativity', 'Creativity & Innovation'),

        ('others', 'Others'),

    )

    instructor = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    title = models.CharField(max_length=200)

    description = models.TextField()

    course_type = models.CharField(
        max_length=50,
        choices=COURSE_TYPES,
        default='technology'
    )

    thumbnail = models.ImageField(
        upload_to='thumbnails/'
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):

        return self.title



# the lesson model

class Lesson(models.Model):

    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='lessons'
    )

    title = models.CharField(max_length=200)

    youtube_link = youtube_link = models.TextField()

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):

        return self.title
    
class Enrollment(models.Model):

    student = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE
    )

    enrolled_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):

        return f"{self.student.username} enrolled in {self.course.title}"
    


class Progress(models.Model):

    student = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE
    )

    completed_lessons = models.ManyToManyField(
        Lesson,
        blank=True
    )

    progress_percentage = models.IntegerField(
        default=0
    )

    def __str__(self):

        return f"{self.student.username} - {self.course.title}"
    

class Notice(models.Model):

    instructor = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    title = models.CharField(
        max_length=200
    )

    message = models.TextField()

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):

        return self.title
    


class TeacherRequest(models.Model):

    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    )

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    full_name = models.CharField(max_length=200)

    email = models.EmailField()

    skills = models.CharField(max_length=300)

    experience = models.TextField()

    reason = models.TextField()

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.full_name