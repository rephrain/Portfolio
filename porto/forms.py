# forms.py
from django import forms

class ContactForm(forms.Form):
    # Define common styling attributes once
    base_widget_attrs = {
        'class': 'w-full px-4 py-2 rounded-md border border-gray-300 dark:border-gray-600 '
                'bg-white dark:bg-gray-800 text-gray-800 dark:text-gray-200 '
                'focus:outline-none focus:ring-2 focus:ring-primary-light dark:focus:ring-primary-dark '
                'transition-colors duration-200',
    }
    
    # Form fields with DRY implementation
    name = forms.CharField(
        max_length=100, 
        widget=forms.TextInput(attrs={
            **base_widget_attrs,
            'placeholder': 'Your Name'
        })
    )
    
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            **base_widget_attrs,
            'placeholder': 'your.email@example.com'
        })
    )
    
    message = forms.CharField(
        widget=forms.Textarea(attrs={
            **base_widget_attrs,
            'rows': 4,
            'placeholder': 'How can I help you?'
        })
    )