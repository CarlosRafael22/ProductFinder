from django.shortcuts import render
import sys
sys.path.insert(1, 'C:\\Users\\carlo\\Documents\\ESTUDOS\\WebScraping\\FurnitureScraping\\')
# from ../../../WebScraping.FurnitureScraping.extractor import PageExtractor

# Create your views here.
def render_main(request):
    from extractor import PageExtractor, DataRetriever
    # import pdb; pdb.set_trace()
    page = PageExtractor('magazineluiza')
    products_dicts = page.query_webdriver('cadeira gamer')

    page = PageExtractor('submarino')
    products_dicts2 = page.query_webdriver('cadeira gamer')

    selected_products = products_dicts[:10] + products_dicts2[:10]
    # page.store_products_on_json(selected_products, 'products.json')

    # selected_products = DataRetriever.get_products_from_json('products.json')

    context = {'products': selected_products}
    return render(request, 'finder/main.html', context)