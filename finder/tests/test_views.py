from finder.views import *
from finder.models import Product, User, Customer
from django.urls import reverse
import json
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


class TestRetrieveProductsAPIView:
    def test_should_retrieve_products(self, client):
        from finder.services import retrieve_products_from_json, create_product_model_from_dict
        import json

        # Putting test products on database
        products_objects = retrieve_products_from_json('test_show_products.json')
        previous_database_total = Product.objects.count()
        for prod in products_objects:
            create_product_model_from_dict(prod.__dict__)
        current_database_total = Product.objects.count()
        assert previous_database_total != current_database_total

        show_url = reverse_querystring('retrieve-products', query_kwargs={'price__gte': 70})

        response = client.get(show_url)
        assert response.status_code == 200
        # import pdb; pdb.set_trace()

        json_response = json.loads(response.content)
        products = json_response['products']
        assert type(products) == list
        assert products[0]['name'] is not None
        assert products[0].get('store', None) is not None


class TestCustomerSignUp:
    from finder.views import CustomerSignupAPI

    def test_should_not_succeed_due_to_email_already_used(self, client):
        # Creating the User with the email
        user = User.objects.create_user('test@mail.com', 'test@mail.com', 'testmail')
        data = {
            'name': 'Teste',
            'username': 'test@mail.com',
            'email': 'test@mail.com',
            'password': 'asdasdadaas'
        }

        signup_url = reverse('signup')
        response = client.post(signup_url, data=data)
        json_response = json.loads(response.content)

        assert response.status_code == 400
        assert json_response['error'] == CustomerSignupAPI.email_error_message
    
    def test_should_not_succeed_due_to_password_under_limit(self, client):
        # Creating the User with the email
        # user = User.objects.create_user('test@mail.com', 'test@mail.com', 'testmail')
        data = {
            'name': 'Teste',
            'username': 'test@mail.com',
            'email': 'test@mail.com',
            'password': 'asdas'
        }

        signup_url = reverse('signup')
        response = client.post(signup_url, data=data)
        json_response = json.loads(response.content)

        assert response.status_code == 400
        assert json_response['error'] == CustomerSignupAPI.password_error_message
    
    def test_should_not_succeed_due_to_missing_field(self, client):
        # Creating the User with the email
        # user = User.objects.create_user('test@mail.com', 'test@mail.com', 'testmail')
        data = {
            'username': 'test@mail.com',
            'email': 'test@mail.com',
            'password': 'asdas'
        }

        signup_url = reverse('signup')
        response = client.post(signup_url, data=data)
        json_response = json.loads(response.content)

        assert response.status_code == 400
        assert json_response['error'] == CustomerSignupAPI.fields_error_message

    def test_should_succeed(self, client):
        data = {
            'name': 'Teste',
            'username': 'test@mail.com',
            'email': 'test@mail.com',
            'password': 'asdasdadaas'
        }

        signup_url = reverse('signup')
        response = client.post(signup_url, data=data)
        json_response = json.loads(response.content)

        assert response.status_code == 200
        assert json_response['customer']['name'] == data['name']
        assert json_response['customer']['user']['username'] == data['username']
        assert json_response['customer']['user']['email'] == data['email']

        customer = Customer.objects.latest('id')
        assert customer.name == data['name']
        assert customer.user.email == data['email']

        user = User.objects.latest('id')
        assert user.email == data['email']
        assert user.username == data['username']