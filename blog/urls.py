from django.urls import path
from django.views.decorators.cache import cache_page

import views

app_name = "blog"
urlpatterns = [
    path(r'', views.IndexView.as_view(), name='index'),
]
