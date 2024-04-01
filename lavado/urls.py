from django.urls import path
from .views import lavado_view

urlpatterns = [
    path('', lavado_view, name='lavado'),
]
