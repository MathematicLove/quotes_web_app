from django.db import models
from django.core.exceptions import ValidationError
from django.db.models.functions import Lower
from django.db.models import Q
from django.utils.text import slugify

class Source(models.Model):
    TYPE_CHOICES = (
        ('movie', 'Фильм'),
        ('book', 'Книга'),
        ('other', 'Другое'),
    )
    title = models.CharField('Название источника', max_length=255, unique=True)
    kind = models.CharField('Тип', max_length=16, choices=TYPE_CHOICES, default='movie')
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    image_url = models.URLField('URL картинки', blank=True, null=True,
                                help_text='Можно оставить пустым — подберём автоматически (Wikipedia).')

    def save(self, *args, **kwargs):
        if not self.slug or self.slug.strip() == '':
            base_slug = slugify(self.title)
            if not base_slug:
                base_slug = 'source'
            
            slug = base_slug
            counter = 1
            while Source.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
                if counter > 1000:
                    break
            
            self.slug = slug[:255]
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

class Quote(models.Model):
    source = models.ForeignKey(Source, on_delete=models.CASCADE, related_name='quotes', verbose_name='Источник')
    text = models.TextField('Цитата')
    weight = models.PositiveIntegerField('Вес', default=1, help_text='Чем больше вес, тем выше шанс показа.')
    is_active = models.BooleanField('Активна', default=True)
    views = models.PositiveIntegerField('Просмотры', default=0)
    likes = models.IntegerField('Лайки', default=0)
    dislikes = models.IntegerField('Дизлайки', default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                Lower('text'), 'source', name='uq_quote_text_source_ci'
            ),
        ]
        indexes = [
            models.Index(fields=['source', 'is_active']),
            models.Index(fields=['-likes', 'source']),
        ]
        ordering = ['-created_at']

    def clean(self):
        if self.is_active:
            qs = Quote.objects.filter(source=self.source, is_active=True)
            if self.pk:
                qs = qs.exclude(pk=self.pk)
            if qs.count() >= 3:
                raise ValidationError('У этого источника уже есть 3 активные цитаты.')

        if self.weight < 1:
            raise ValidationError('Вес должен быть >= 1.')

    def __str__(self):
        return f'«{self.text[:50]}...» — {self.source.title}'
