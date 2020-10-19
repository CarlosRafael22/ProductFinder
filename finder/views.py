from django.shortcuts import render
from django.http import JsonResponse
from django.views import View
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


# Create your views here.
def render_main(request):
    products = retrieve_products_from_json('search_products.json')

    query_keys_list = [*request.GET]
    filtered_products = products
    # If it comes with params then we need to filter before sending response
    
    if len(query_keys_list) > 0:
        parsed_query = {}
        for key, value in request.GET.items():
            if 'order_by_' not in key:
                parsed_query[key] = float(value) if 'contains' not in key else value
                attribute = None
                order = None
            else:
                # If there is an order_by params we get the attribute its sorting and order
                attribute = key.split('order_by_')[1]
                order = value


        filtered_products = ProductDatabase.filter(**parsed_query)
        print(filtered_products)
        # If there is an order_by params we get the attribute its sorting and order
        if attribute and order:
            reversed = order == 'desc'
            filtered_products.sort(key=lambda prod: getattr(prod, attribute), reverse=reversed)
        print(filtered_products)

    context = {'products': filtered_products, 'products_total': len(filtered_products)}
    return render(request, 'finder/main.html', context)


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


def search_products_with_query(request, query_word):
    if request.method == 'GET':
        parsed_query = query_word.replace('-', ' ')
        products_dicts = get_products_from_query(parsed_query)

        # Saving on JSON for the template to show data from this
        save_products_on_json(products_dicts, 'search_products.json')
        # import pdb; pdb.set_trace()
        return JsonResponse({'products': products_dicts})