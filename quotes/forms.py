from django import forms
from .models import Quote


class QuoteForm(forms.ModelForm):
    """Formulaire pour ajouter une citation."""
    
    class Meta:
        model = Quote
        fields = ['text', 'author']
        widgets = {
            'text': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Entrez la citation...',
                'rows': 4
            }),
            'author': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nom de l\'auteur'
            })
        }
