from django.shortcuts import render
from django.http import JsonResponse
from django.views import View
from django.core import serializers
from typing import List
import sys
sys.path.insert(1, 'C:\\Users\\carlo\\Documents\\ESTUDOS\\Web Scraping\\Furniture Scraping\\')
from extractor import PageExtractor, DataRetriever
from products import Product as ProductObject, ProductDatabase
from .models import Product


# Create your views here.
def render_main(request):
    from .services import retrieve_products_from_json

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


# def search_products_with_query(request, query_word):
#     if request.method == 'GET':
#         parsed_query = query_word.replace('-', ' ')
#         products_dicts = get_products_from_query(parsed_query)

#         # Saving on JSON for the template to show data from this
#         save_products_on_json(products_dicts, 'search_products.json')
#         # import pdb; pdb.set_trace()
#         return JsonResponse({'products': products_dicts})


class SearchProductsWithQueryView(View):
    def get(self, request, **kwargs):
        from .services import search_products_with_query

        data_with_only_fields = search_products_with_query(self.kwargs['query_word'])

        return JsonResponse({'products': data_with_only_fields})


class ShowProductsStoredOnDatabaseView(View):
    def get(self, request):
        from django.core import serializers
        import json
        from .services import show_products_stored_on_database
        filtered_products = show_products_stored_on_database(request.GET)

        # Manually serializing since its not using DRF yet
        data = serializers.serialize('json', filtered_products)
        data_with_only_fields = [prod['fields'] for prod in json.loads(data)]

        context = {'products': data_with_only_fields, 'products_total': filtered_products.count()}
        return render(request, 'finder/main.html', context)


class RetrieveProductsAPI(View):
    def get(self, request):
        from .services import show_products_stored_on_database
        import json

        filtered_products = show_products_stored_on_database(request.GET)

        # Manually serializing since its not using DRF yet
        data = serializers.serialize('json', filtered_products)
        data_with_only_fields = [prod['fields'] for prod in json.loads(data)]

        response = {'products': data_with_only_fields}
        return JsonResponse(response)