from django.urls import path
from . import views

app_name = 'quotes'

urlpatterns = [
    path('', views.home, name='home'),
    path('add/', views.add_quote, name='add'),
    path('top/', views.top_quotes, name='top'),
    path('search/', views.search_by_source, name='search'),
    path('api/random/', views.api_random, name='api_random'),
    path('api/quote/<int:pk>/<str:action>/', views.like_dislike, name='like_dislike'),
    path('healthcheck/', views.healthcheck, name='healthcheck'),
]
