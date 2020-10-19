from django.core import serializers
from typing import List
import sys
sys.path.insert(1, 'C:\\Users\\carlo\\Documents\\ESTUDOS\\Web Scraping\\Furniture Scraping\\')
from extractor import PageExtractor, DataRetriever
from products import Product as ProductObject, ProductDatabase
from .models import Product

def get_products_from_query(query: str) -> List[dict]:
    ''' Returns a list of dictionaries with the products queried with the DataRetriever query_for method '''
    retriever = DataRetriever(['submarino', 'extra'])
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
            name=product_dict['name'],
            price=product_dict['price'],
            link=product_dict['link'],
            image_url=product_dict['image_url'],
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