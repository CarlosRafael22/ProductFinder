from finder.views import *
from finder.models import Product
import pytest
pytestmark = pytest.mark.django_db

class TestViews:
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


class TestModelCreation:
    def test_should_create_product_model_from_dict(self):
        prod_dict = {
            'name': 'Camera GOPRO HERO 10 Black',
            'price_str': 'R$ 4.299,90',
            'price': 4299.90,
            'link': 'link_url',
            'image_url': 'image_url',
            'store': 'americanas'
        }

        product = create_product_model_from_dict(prod_dict)
        assert type(product) == Product
        assert product.name == prod_dict['name']
        assert product.price == prod_dict['price']
        assert product.store == prod_dict['store']
