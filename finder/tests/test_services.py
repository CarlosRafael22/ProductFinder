from finder.services import *
from finder.models import Product
import pytest
pytestmark = pytest.mark.django_db

class TestServicesMethods:
    # def test_should_get_products_from_query(self):
    #     import os
    #     products_dicts = get_products_from_query('cadeira gamer')
    #     assert type(products_dicts[0]) == dict

    #     file_name = 'test.json'
    #     if os.path.exists(file_name):
    #         os.remove(file_name)
    #     save_products_on_json(products_dicts, file_name)
    #     assert os.path.exists(file_name) == True, 'Should have saved products dicts on json'

    # def test_should_retrieve_products_from_json(self):
    #     import os
    #     file_name = 'test.json'
    #     if os.path.exists(file_name):
    #         products = retrieve_products_from_json(file_name)
    #         assert products[0] != None
    #     else:
    #         with pytest.raises(Exception):
    #             products = retrieve_products_from_json(file_name)

    @pytest.mark.parametrize('query_dict,expected_products_list', [
        ({'price__lt': 75}, ["Livro - Harry Potter and the Goblet of Fire", "Usado: Harry Potter and the Goblet of Fire (Ingl\u00eas) Capa comum"]),
        ({'price__lt': 75, 'order_by_price': 'desc'}, ["Usado: Harry Potter and the Goblet of Fire (Ingl\u00eas) Capa comum", "Livro - Harry Potter and the Goblet of Fire"]),
        ({}, [
            "Livro - Harry Potter and the Goblet of Fire", "Harry Potter And The Goblet Of Fire", "Usado: Harry Potter and the Goblet of Fire (Ingl\u00eas) Capa comum",
            "Harry Potter and the Goblet of Fire (Video Game)", "Dementor And Harry Potter 1/8 Two-pack - Harry Potter And The Goblet Of Fire - Star Ace"
        ])
    ])
    def test_should_show_products_stored_on_database(self, query_dict, expected_products_list):
        # Putting test products on database
        products_objects = retrieve_products_from_json('test_show_products.json')
        previous_database_total = Product.objects.count()
        for prod in products_objects:
            create_product_model_from_dict(prod.__dict__)
        current_database_total = Product.objects.count()
        assert previous_database_total != current_database_total

        # Filtering the products to be shown
        filtered_products = show_products_stored_on_database(query_dict)
        assert len(filtered_products) == len(expected_products_list)
        products_names = [prod.name for prod in filtered_products]
        assert products_names == expected_products_list
        


class oTestModelCreation:
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