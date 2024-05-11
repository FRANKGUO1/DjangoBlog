from django.urls import path
from django.views.decorators.cache import cache_page

from . import views

app_name = "blog"
urlpatterns = [
    path(r'', 
         views.IndexView.as_view(), 
         name='index'),
]
