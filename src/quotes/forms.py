from django import forms
from .models import Source, Quote

class SourceForm(forms.ModelForm):
    class Meta:
        model = Source
        fields = ('title', 'kind', 'image_url')

class QuoteForm(forms.ModelForm):
    class Meta:
        model = Quote
        fields = ('source', 'text', 'weight', 'is_active')
        widgets = {
            'text': forms.Textarea(attrs={'rows': 3})
        }

class QuickQuoteCreateForm(forms.Form):
    source_title = forms.CharField(label='Название источника', max_length=255)
    source_kind = forms.ChoiceField(label='Тип', choices=Source.TYPE_CHOICES, initial='movie')
    image_url = forms.URLField(label='URL картинки', required=False)
    quote_text = forms.CharField(label='Цитата', widget=forms.Textarea(attrs={'rows': 3}))
    weight = forms.IntegerField(label='Вес', min_value=1, initial=1)
    is_active = forms.BooleanField(label='Активна', required=False, initial=True)
