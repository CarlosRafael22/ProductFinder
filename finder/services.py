from django.core import serializers
from typing import List
import sys
sys.path.insert(1, 'C:\\Users\\carlo\\Documents\\ESTUDOS\\Web Scraping\\Furniture Scraping\\')
from extractor import PageExtractor, DataRetriever
from products import Product as ProductObject, ProductDatabase
from .models import Product, Customer, User

def get_products_from_query(query: str) -> List[dict]:
    ''' Returns a list of dictionaries with the products queried with the DataRetriever query_for method '''
    retriever = DataRetriever(['submarino', 'extra', 'magazineluiza'])
    products_dicts = retriever.query_for(query)
    return products_dicts


def save_products_on_json(products_dicts: List[dict], file_name: str):
    ''' Saves the dictionaries of products on json file '''
    DataRetriever.store_products_on_json(products_dicts, file_name)


def retrieve_products_from_json(file_name: str) -> List[ProductObject]:
    ''' Loads list of products from json file '''
    products = DataRetriever.get_products_from_json(file_name)
    return products


def is_product_on_database(product_dict):
    ''' Checks whether product has already been inserted by some fields on the dictionary '''
    try:
        Product.objects.get(name=product_dict['name'], store=product_dict['store'], price=product_dict['price'])
        return True
    except Product.DoesNotExist:
        return False


def create_product_model_from_dict(product_dict):
    ''' Creates product on the server from its dictionary after checking it hasnt been already inserted in the database '''
    if not is_product_on_database(product_dict):
        product = Product.objects.create(
            name=product_dict['name'][:200],
            price=product_dict['price'],
            link=product_dict['link'][:200],
            image_url=product_dict['image_url'][:200],
            store=product_dict['store'])
    else:
        product = None
    return product


def search_products_with_query(query_word):
    import json
    parsed_query = query_word.replace('-', ' ')
    products_dicts = get_products_from_query(parsed_query)

    # Saving on JSON for the template to show data from this
    save_products_on_json(products_dicts, 'search_products.json')

    # Saves products on database
    newly_created_products = []
    for prod_dict in products_dicts:
        created_product = create_product_model_from_dict(prod_dict)
        if created_product:
            newly_created_products.append(created_product)
    
    # Get the database products serialized to be sent as response then we already filter out the dictionaries which had the same products
    # products = Product.objects.filter(id__in=[prod.id for prod in newly_created_products])
    data = serializers.serialize('json', newly_created_products)
    data_with_only_fields = [prod['fields'] for prod in json.loads(data)]
    return data_with_only_fields


def show_products_stored_on_database(query_filters_dict):
    '''
    
    @query_filters_dict: {
        'price__gte': 60
        'price__lt': 89
        'order_by_price': 'desc' / 'asc'
    }
    '''
    products = Product.objects.all()

    query_keys_list = [*query_filters_dict]
    filtered_products = products
    # If it comes with params then we need to filter before sending response
    
    if len(query_keys_list) > 0:
        parsed_query = {}
        for key, value in query_filters_dict.items():
            if 'order_by_' not in key:
                parsed_query[key] = float(value) if 'contains' not in key else value
                attribute = None
                order = None
            else:
                # If there is an order_by params we get the attribute its sorting and order
                attribute = key.split('order_by_')[1]
                order = value

        # filtered_products = ProductDatabase.filter(**parsed_query)
        filtered_products = Product.objects.filter(**parsed_query)
        print(filtered_products)
        # If there is an order_by params we get the attribute its sorting and order
        if attribute and order:
            # reversed = order == 'desc'
            # filtered_products.sort(key=lambda prod: getattr(prod, attribute), reverse=reversed)
            filter_order = '-' if order == 'desc' else ''
            order_as = filter_order + attribute
            filtered_products = filtered_products.order_by(order_as)
        print(filtered_products)
    return filtered_products


def handle_customer_signup(request_data: dict):
    '''
        data = {
            'name': 'Teste',
            'username': 'test@mail.com',
            'email': 'test@mail.com',
            'password': 'asdas'
        }
    '''
    from .views import CustomerSignupAPI
    from .serializers import CustomerSerializer

    try:
        email = request_data['email']
        username = request_data['username']
        name = request_data['name']
        password = request_data['password']
    except Exception as excp:
        raise Exception(CustomerSignupAPI.fields_error_message)

    if len(password) < 6:
        raise Exception(CustomerSignupAPI.password_error_message)

    try:
        user = User.objects.create_user(username, email, password)
    except Exception as excp:
        raise Exception(CustomerSignupAPI.email_error_message)

    try:
        customer = Customer.objects.create(name=name, user=user)
        response = CustomerSerializer(customer)
        return response
    except Exception as excp:
        raise excp
