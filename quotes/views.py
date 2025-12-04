from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.core.paginator import Paginator
from .models import Quote
from .forms import QuoteForm
import random
import logging

logger = logging.getLogger(__name__)

def home(request):
    """Page d'accueil avec une citation aléatoire."""
    quotes = Quote.objects.all()
    random_quote = random.choice(quotes) if quotes.exists() else None
    
    logger.info("Ma vue a été appelée")
    logger.debug("Données reçues : %s", request.GET.dict())

    context = {
        'random_quote': random_quote,
        'total_quotes': quotes.count()
    }
    return render(request, 'quotes/home.html', context)


def quote_list(request):
    """Liste de toutes les citations avec pagination."""
    quotes = Quote.objects.all()
    paginator = Paginator(quotes, 6)  # 6 citations par page
    
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'total_quotes': quotes.count()
    }
    return render(request, 'quotes/quote_list.html', context)


def quote_create(request):
    """Créer une nouvelle citation."""
    if request.method == 'POST':
        form = QuoteForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, '✅ Citation ajoutée avec succès !')
            return redirect('quote_list')
    else:
        form = QuoteForm()
    
    context = {'form': form}
    return render(request, 'quotes/quote_form.html', context)


def quote_delete(request, pk):
    """Supprimer une citation."""
    quote = get_object_or_404(Quote, pk=pk)
    
    if request.method == 'POST':
        quote.delete()
        messages.success(request, '🗑️ Citation supprimée avec succès !')
        return redirect('quote_list')
    
    context = {'quote': quote}
    return render(request, 'quotes/quote_confirm_delete.html', context)


def health(request):
    """Endpoint de santé pour le monitoring."""
    from django.http import JsonResponse
    return JsonResponse({'status': 'ok', 'app': 'quotes'})
