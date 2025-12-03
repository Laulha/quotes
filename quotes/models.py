from django.db import models
from django.utils import timezone


class Quote(models.Model):
    """Modèle représentant une citation."""
    
    text = models.TextField(
        verbose_name="Texte de la citation",
        help_text="Le contenu de la citation"
    )
    author = models.CharField(
        max_length=200,
        verbose_name="Auteur",
        help_text="Nom de l'auteur de la citation"
    )
    created_at = models.DateTimeField(
        default=timezone.now,
        verbose_name="Date de création"
    )
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = "Citation"
        verbose_name_plural = "Citations"
    
    def __str__(self):
        return f"{self.author} - {self.text[:50]}..."
