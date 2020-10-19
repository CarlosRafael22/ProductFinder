from finder.views import *
from finder.models import Product
from django.urls import reverse
import pytest
pytestmark = pytest.mark.django_db


class TestSearchProductsWithQueryView:
    def test_should_search_products_with_query(self, client):
        import json

        previous_database_total = Product.objects.count()

        search_url = reverse('finder-search', args=['goblet-of-fire'])
        response = client.get(search_url)
        json_response = json.loads(response.content)
        products_dicts = json_response['products']

        assert type(products_dicts) == list
        # If there are products then check whether the first has these attributes
        if len(products_dicts) > 0:
            assert products_dicts[0].get('name', None) is not None
            assert products_dicts[0].get('price', None) is not None
            assert products_dicts[0].get('link', None) is not None

        # Checks whether the database was populated
        database_products = Product.objects.all()
        if len(products_dicts) > 0:
            assert database_products.count() > previous_database_total
            # Since when creating products on database it checks whether its been already inserted the total might not be the same
            assert len(products_dicts) >= database_products.count()

# CANT USE query string params on reverse so found this modification on the internet
# https://gist.github.com/benbacardi/227f924ec1d9bedd242b
def reverse_querystring(view, urlconf=None, args=None, kwargs=None, current_app=None, query_kwargs=None):
    '''Custom reverse to handle query strings.
    Usage:
        reverse('app.views.my_view', kwargs={'pk': 123}, query_kwargs={'search': 'Bob'})
    '''
    from django.utils.http import urlencode

    base_url = reverse(view, urlconf=urlconf, args=args, kwargs=kwargs, current_app=current_app)
    if query_kwargs:
        return '{}?{}'.format(base_url, urlencode(query_kwargs))
    return base_url

class TestShowProductsStoredOnDatabaseView:
    def test_should_show_products(self, client):
        from finder.services import retrieve_products_from_json, create_product_model_from_dict
        import json

        # Putting test products on database
        products_objects = retrieve_products_from_json('test_show_products.json')
        previous_database_total = Product.objects.count()
        for prod in products_objects:
            create_product_model_from_dict(prod.__dict__)
        current_database_total = Product.objects.count()
        assert previous_database_total != current_database_total

        show_url = reverse_querystring('finder-show', query_kwargs={'price__gte': 70})
        response = client.get(show_url)
        assert response.status_code == 200
