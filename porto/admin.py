from django.contrib import admin
from .models import Resume,Color, SkillCategory, Skill, Project, Articles, ContactSubmission

admin.site.register(Resume)
admin.site.register(Color)
admin.site.register(SkillCategory)
admin.site.register(Skill)
admin.site.register(Project)
admin.site.register(Articles)
@admin.register(ContactSubmission)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'created_at')
    search_fields = ('name', 'email', 'message')
    readonly_fields = ('created_at',)
# Register your models here.
