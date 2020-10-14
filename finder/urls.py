from django.urls import path
from . import views

urlpatterns = [
    path('', views.render_main, name='finder-main'),
    path('search/<str:query_word>', views.find_products_with_query, name='finder-search'),
]
