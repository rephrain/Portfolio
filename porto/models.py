from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class Resume(models.Model):
    file = models.FileField(upload_to='resumes/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.file.name} - {self.uploaded_at}"

class Articles(models.Model):
    image = models.ImageField(upload_to='static/img') 
    title = models.CharField(max_length=200)
    content = models.TextField()
    link = models.URLField(max_length=200, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.title

class Testimonial(models.Model):
    name = models.CharField(max_length=100)
    position = models.CharField(max_length=200)
    company = models.CharField(max_length=200)
    content = models.TextField()
    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    
    def __str__(self):
        return f"{self.name} - {self.company}"

class ContactSubmission(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Message from {self.name} ({self.created_at.strftime('%Y-%m-%d')})"

class SkillCategory(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(unique=True)
    
    class Meta:
        verbose_name_plural = "Skill Categories"
    
    def __str__(self):
        return self.name
    
class Color(models.Model):
    category = models.OneToOneField(
        SkillCategory,
        to_field='slug',
        db_column='category_slug',
        on_delete=models.CASCADE,
        primary_key=True 
    )
    color = models.CharField(max_length=20, help_text="Tailwind base color, e.g., 'blue'")

    def __str__(self):
        return f"{self.category.name} - {self.color}"
    
class Skill(models.Model):
    name = models.CharField(max_length=100)
    level = models.IntegerField(default=0)
    description = models.TextField()
    category = models.ForeignKey(SkillCategory, related_name='skills', on_delete=models.CASCADE)
    
    class Meta:
        ordering = ['-level']
    
    def __str__(self):
        return f"{self.name} ({self.category.name})"
    
class Project(models.Model):
    image = models.ImageField(upload_to='static/img', null=True) 
    title = models.CharField(max_length=200)
    category = models.ForeignKey(SkillCategory, related_name='projects', on_delete=models.CASCADE)
    description = models.TextField()
    skill = models.ManyToManyField(Skill, related_name='projects')
    link = models.URLField(max_length=200, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return self.title