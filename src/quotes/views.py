from django.db.models import F
from django.http import JsonResponse, Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.decorators.http import require_POST, require_GET

from .models import Quote, Source
from .forms import QuoteForm, SourceForm, QuickQuoteCreateForm
from .utils import weighted_choice, wikipedia_thumb_for_title

def home(request):
    qs = Quote.objects.filter(is_active=True).select_related('source')
    if not qs.exists():
        return render(request, 'quotes/home.html', {'quote': None, 'msg': 'Пока нет активных цитат.'})

    pair_list = [(q, max(1, q.weight)) for q in qs]
    quote = weighted_choice(pair_list)

    Quote.objects.filter(pk=quote.pk).update(views=F('views') + 1)

    image_url = quote.source.image_url or wikipedia_thumb_for_title(quote.source.title)
    return render(request, 'quotes/home.html', {'quote': quote, 'image_url': image_url})

def add_quote(request):
    if request.method == 'POST':
        qform = QuoteForm(request.POST)
        sform = SourceForm(request.POST)
        if qform.is_valid():
            quote = qform.save(commit=False)
            quote.full_clean()
            quote.save()
            return redirect('quotes:home')
    else:
        qform = QuoteForm()
        sform = SourceForm()
    return render(request, 'quotes/add_quote.html', {'qform': qform, 'sform': sform})

@require_POST
def like_dislike(request, pk: int, action: str):
    quote = get_object_or_404(Quote, pk=pk)
    if action == 'like':
        Quote.objects.filter(pk=pk).update(likes=F('likes') + 1)
    elif action == 'dislike':
        Quote.objects.filter(pk=pk).update(dislikes=F('dislikes') + 1)
    else:
        raise Http404()
    quote.refresh_from_db(fields=['likes', 'dislikes'])
    return JsonResponse({'likes': quote.likes, 'dislikes': quote.dislikes})

def top_quotes(request):
    qs = Quote.objects.order_by('-likes', '-views').select_related('source')[:10]
    return render(request, 'quotes/top.html', {'quotes': qs})

def search_by_source(request):
    query = request.GET.get('q', '').strip()
    found_source = None
    quotes = []
    quick_form = QuickQuoteCreateForm()

    if query:
        found_source = Source.objects.filter(title__iexact=query).first()
        if found_source:
            quotes = Quote.objects.filter(source=found_source).order_by('-likes', '-views')
        else:
            quick_form = QuickQuoteCreateForm(initial={'source_title': query})

    if request.method == 'POST' and not found_source:
        quick_form = QuickQuoteCreateForm(request.POST)
        if quick_form.is_valid():
            src, _ = Source.objects.get_or_create(
                title=quick_form.cleaned_data['source_title'],
                defaults={
                    'kind': quick_form.cleaned_data['source_kind'],
                    'image_url': quick_form.cleaned_data.get('image_url') or ''
                }
            )
            quote = Quote(
                source=src,
                text=quick_form.cleaned_data['quote_text'],
                weight=quick_form.cleaned_data['weight'],
                is_active=quick_form.cleaned_data['is_active'],
            )
            quote.full_clean()
            quote.save()
            return redirect(f"{reverse('quotes:search')}?q={src.title}")

    return render(request, 'quotes/search.html', {
        'query': query, 'source': found_source, 'quotes': quotes, 'quick_form': quick_form
    })

@require_GET
def api_random(request):
    qs = Quote.objects.filter(is_active=True).select_related('source')
    if not qs.exists():
        return JsonResponse({'error': 'no_active_quotes'}, status=404)
    pair_list = [(q, max(1, q.weight)) for q in qs]
    q = weighted_choice(pair_list)
    return JsonResponse({
        'id': q.id, 'text': q.text, 'source': q.source.title, 'weight': q.weight,
        'likes': q.likes, 'dislikes': q.dislikes, 'views': q.views
    })

def healthcheck(request):
    try:
        _ = Source.objects.first()
        ok = True
    except Exception:
        ok = False
    return render(request, 'quotes/healthcheck.html', {'ok': ok})
