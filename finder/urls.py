from django.urls import path
from . import views

urlpatterns = [
    # path('', views.render_main, name='finder-main'),
    path('', views.ShowProductsStoredOnDatabaseView.as_view(), name='finder-show'),
    # path('search/<str:query_word>', views.search_products_with_query, name='finder-search'),
    path('search/<str:query_word>', views.SearchProductsWithQueryView.as_view(), name='finder-search'),
    path('api/products', views.RetrieveProductsAPI.as_view(), name='retrieve-products'),
]
