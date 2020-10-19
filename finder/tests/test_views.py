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