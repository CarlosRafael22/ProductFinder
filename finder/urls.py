from django.urls import path
from . import views

urlpatterns = [
    path('', views.render_main, name='finder-main'),
]
