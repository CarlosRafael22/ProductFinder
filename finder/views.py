from django.shortcuts import render
from django.http import JsonResponse
from typing import List
import sys
sys.path.insert(1, 'C:\\Users\\carlo\\Documents\\ESTUDOS\\Web Scraping\\Furniture Scraping\\')
from extractor import PageExtractor, DataRetriever
from products import Product


def get_products_from_query(query: str) -> List[dict]:
    ''' Returns a list of dictionaries with the products queried with the DataRetriever query_for method '''
    retriever = DataRetriever(['americanas', 'submarino'])
    products_dicts = retriever.query_for(query)
    return products_dicts


def save_products_on_json(products_dicts: List[dict], file_name: str):
    ''' Saves the dictionaries of products on json file '''
    DataRetriever.store_products_on_json(products_dicts, file_name)


def retrieve_products_from_json(file_name: str) -> List[Product]:
    ''' Loads list of products from json file '''
    products = DataRetriever.get_products_from_json(file_name)
    return products


# Create your views here.
def render_main(request):
    # from extractor import PageExtractor, DataRetriever
    # # import pdb; pdb.set_trace()
    # page = PageExtractor('magazineluiza')
    # products_dicts = page.query_webdriver('cadeira gamer')

    # page = PageExtractor('submarino')
    # products_dicts2 = page.query_webdriver('cadeira gamer')

    # selected_products = products_dicts[:10] + products_dicts2[:10]
    # page.store_products_on_json(selected_products, 'products.json')

    # selected_products = DataRetriever.get_products_from_json('products.json')
    products = retrieve_products_from_json('search_products.json')

    context = {'products': products, 'products_total': len(products)}
    return render(request, 'finder/main.html', context)


def find_products_with_query(request, query_word):
    parsed_query = query_word.replace('-', ' ')
    products_dicts = get_products_from_query(parsed_query)

    # Saving on JSON for the template to show data from this
    save_products_on_json(products_dicts, 'search_products.json')
    # import pdb; pdb.set_trace()
    return JsonResponse({'products': products_dicts})