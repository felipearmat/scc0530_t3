from django.urls import path, re_path
from . import views
# Um namespace para que as urls sejam chamadas facilmente nos templates.
app_name = 'base'

# Caminhos da nossa aplicação que referenciam uma função em views.py
urlpatterns = [
    path('', views.HomeView.as_view(), name='index'),
    re_path(r'^.*/$', views.HomeView.as_view(), name='reindex'),
]
