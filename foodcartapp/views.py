import json

from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.templatetags.static import static


from .models import Product, Order, OrderElements


def banners_list_api(request):
    # FIXME move data to db?
    return JsonResponse([
        {
            'title': 'Burger',
            'src': static('burger.jpg'),
            'text': 'Tasty Burger at your door step',
        },
        {
            'title': 'Spices',
            'src': static('food.jpg'),
            'text': 'All Cuisines',
        },
        {
            'title': 'New York',
            'src': static('tasty.jpg'),
            'text': 'Food is incomplete without a tasty dessert',
        }
    ], safe=False, json_dumps_params={
        'ensure_ascii': False,
        'indent': 4,
    })


def product_list_api(request):
    products = Product.objects.select_related('category').available()

    dumped_products = []
    for product in products:
        dumped_product = {
            'id': product.id,
            'name': product.name,
            'price': product.price,
            'special_status': product.special_status,
            'description': product.description,
            'category': {
                'id': product.category.id,
                'name': product.category.name,
            } if product.category else None,
            'image': product.image.url,
            'restaurant': {
                'id': product.id,
                'name': product.name,
            }
        }
        dumped_products.append(dumped_product)
    return JsonResponse(dumped_products, safe=False, json_dumps_params={
        'ensure_ascii': False,
        'indent': 4,
    })


def register_order(request):
    food_order = json.loads(request.body.decode())

    order, created = Order.objects.get_or_create(
        firstname=food_order['firstname'],
        lastname=food_order['lastname'],
        phonenumber=food_order['phonenumber'],
        address=food_order['address'],
    )

    for product_order in food_order['products']:
        product = get_object_or_404(Product.objects.prefetch_related('products'), id=product_order['product'])
        OrderElements.objects.get_or_create(
            order=order,
            product=product,
            count=product_order['quantity']
        )

    return JsonResponse({})
