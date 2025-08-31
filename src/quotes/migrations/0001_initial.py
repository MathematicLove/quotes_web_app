import django.db.models.deletion
import django.db.models.functions.text
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Source',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, unique=True, verbose_name='Название источника')),
                ('kind', models.CharField(choices=[('movie', 'Фильм'), ('book', 'Книга'), ('other', 'Другое')], default='movie', max_length=16, verbose_name='Тип')),
                ('slug', models.SlugField(blank=True, max_length=255, unique=True)),
                ('image_url', models.URLField(blank=True, help_text='Можно оставить пустым — подберём автоматически (Wikipedia).', null=True, verbose_name='URL картинки')),
            ],
        ),
        migrations.CreateModel(
            name='Quote',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(verbose_name='Цитата')),
                ('weight', models.PositiveIntegerField(default=1, help_text='Чем больше вес, тем выше шанс показа.', verbose_name='Вес')),
                ('is_active', models.BooleanField(default=True, verbose_name='Активна')),
                ('views', models.PositiveIntegerField(default=0, verbose_name='Просмотры')),
                ('likes', models.IntegerField(default=0, verbose_name='Лайки')),
                ('dislikes', models.IntegerField(default=0, verbose_name='Дизлайки')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('source', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='quotes', to='quotes.source', verbose_name='Источник')),
            ],
            options={
                'ordering': ['-created_at'],
                'indexes': [models.Index(fields=['source', 'is_active'], name='quotes_quot_source__b75873_idx'), models.Index(fields=['-likes', 'source'], name='quotes_quot_likes_a1fa17_idx')],
                'constraints': [models.UniqueConstraint(django.db.models.functions.text.Lower('text'), models.F('source'), name='uq_quote_text_source_ci')],
            },
        ),
    ]
