from django.shortcuts import render, redirect
from django.urls import reverse
from django.core.paginator import Paginator
from django.contrib import messages
from django.db.models import Q
from .models import Resume, SkillCategory, Project, Articles, ContactSubmission
from .forms import ContactForm
import json
from datetime import date

def home_view(request):
    latest_resume = Resume.objects.last() 
    
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            # Save message to database
            ContactSubmission.objects.create(
                name=form.cleaned_data['name'],
                email=form.cleaned_data['email'],
                message=form.cleaned_data['message']
            )
            messages.success(request, 'Your message has been received. Thank you!')
            return redirect(reverse('home') + '#contact')
    else:
        form = ContactForm()
    
    categories = SkillCategory.objects.select_related('color').all()
    skills_by_category = {}

    category_data = []
    for category in categories:
        skills_by_category[category.slug] = list(
            category.skills.values('name', 'level', 'description')
        )

        color = getattr(category, 'color', None)
        color_name = color.color if color else 'gray'

        category_data.append({
            'name': category.name,
            'slug': category.slug,
            'color': color_name,
        })

    projects_list = Project.objects.prefetch_related('skill__category__color').select_related('category__color').all()

    # Category filter
    category_filter = request.GET.get('category')
    if category_filter:
        projects_list = projects_list.filter(category__slug=category_filter)
    
    # Skill filter
    skill_filter = request.GET.get('skill')
    if skill_filter:
        projects_list = projects_list.filter(skill__id=skill_filter)
    
    # Search functionality
    search_query = request.GET.get('search')
    if search_query:
        projects_list = projects_list.filter(
            Q(title__icontains=search_query) | 
            Q(description__icontains=search_query) |
            Q(skill__name__icontains=search_query)
        ).distinct()
    
    all_project_categories = SkillCategory.objects.select_related('color').prefetch_related('skills').filter(
        projects__isnull=False
    ).distinct()

    project_paginator = Paginator(projects_list, 3)
    project_page_number = request.GET.get('project_page')
    projects = project_paginator.get_page(project_page_number)

    # Articles pagination
    articles_list = Articles.objects.order_by('-created_at')
    article_paginator = Paginator(articles_list, 2)
    article_page_number = request.GET.get('article_page')
    articles = article_paginator.get_page(article_page_number)

    # Add contact form to context
    context = {
        'resume': latest_resume,
        'skills_by_category_json': json.dumps(skills_by_category),
        'categories': category_data,
        'all_categories': all_project_categories,
        'projects': projects,
        'project_paginator': project_paginator,
        'articles': articles,
        'article_paginator': article_paginator,
        'form': form,
        'experience_engineer': round((date.today() - date(2023, 7, 1)).days / 365.25, 2),
        'experience_science': round((date.today() - date(2023, 3, 1)).days / 365.25, 2),
    }

    return render(request, 'home.html', context)