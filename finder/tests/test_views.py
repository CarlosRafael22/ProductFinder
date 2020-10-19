from finder.views import *
from finder.models import Product
from django.urls import reverse
import pytest
pytestmark = pytest.mark.django_db

class oiTestViewsMethods:
    def test_should_get_products_from_query(self):
        import os
        products_dicts = get_products_from_query('cadeira gamer')
        assert type(products_dicts[0]) == dict

        file_name = 'test.json'
        if os.path.exists(file_name):
            os.remove(file_name)
        save_products_on_json(products_dicts, file_name)
        assert os.path.exists(file_name) == True, 'Should have saved products dicts on json'

    def test_should_retrieve_products_from_json(self):
        import os
        file_name = 'test.json'
        if os.path.exists(file_name):
            products = retrieve_products_from_json(file_name)
            assert products[0] != None
        else:
            with pytest.raises(Exception):
                products = retrieve_products_from_json(file_name)


class TestViews:
    def test_should_search_products_with_query(self, client):
        import json
        search_url = reverse('finder-search', args=['goblet of fire'])
        response = client.get(search_url)
        # assert type(response['products']) == list
        json_response = json.loads(response.content)
        products_dicts = json_response['products']
        assert type(products_dicts) == list
        # If there are products then check whether the first has these attributes
        if len(products_dicts) > 0:
            assert products_dicts[0].get('name', None) is not None
            assert products_dicts[0].get('price', None) is not None
            assert products_dicts[0].get('link', None) is not None


class oiTestModelCreation:
    @pytest.mark.parametrize('name,expected_product_type, database_total', [
        ('Camera GOPRO HERO 10 Black', 'NoneType', 1),
        ('Camera GOPRO HERO 7 Silver', 'Product', 2)
    ])
    def test_should_create_product_model_from_dict(self, name, expected_product_type, database_total):
        product_dict = {
            'name': 'Camera GOPRO HERO 10 Black',
            'price_str': 'R$ 4.299,90',
            'price': 4299.90,
            'link': 'link_url',
            'image_url': 'image_url',
            'store': 'americanas'
        }

        product = create_product_model_from_dict(product_dict)
        assert type(product) == Product
        assert product.name == product_dict['name']
        assert product.price == product_dict['price']
        assert product.store == product_dict['store']

        # Creating new dictionary with custom name to check whether is on database or not
        product_dict2 = {**product_dict, 'name': name}
        new_product = create_product_model_from_dict(product_dict2)
        assert new_product.__class__.__name__ == expected_product_type
        assert Product.objects.count() == database_total

    @pytest.mark.parametrize('name,expected_check', [
        ('Camera GOPRO HERO 10 Black', True),
        ('Camera GOPRO HERO 7 Silver', False)
    ])
    def test_should_check_is_product_on_database(self, name, expected_check):
        product_dict = {
            'name': 'Camera GOPRO HERO 10 Black',
            'price_str': 'R$ 4.299,90',
            'price': 4299.90,
            'link': 'link_url',
            'image_url': 'image_url',
            'store': 'americanas'
        }

        create_product_model_from_dict(product_dict)
        # Creating new dictionary with custom name to check whether is on database or not
        product_dict2 = {**product_dict, 'name': name}
        check = is_product_on_database(product_dict2)
        assert check == expected_check
