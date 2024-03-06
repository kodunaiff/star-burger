import phonenumbers
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.templatetags.static import static
from phonenumbers import NumberParseException
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

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


def check_fields(food_order):
    list_key = ['products', 'firstname', 'lastname', 'phonenumber', 'address']
    obligatory_fields = []
    empty_fields = []
    product_amount = Product.objects.all().count()

    for key in list_key:
        try:
            food_order[key]
        except KeyError:
            obligatory_fields.append(key)
    if obligatory_fields:
        content = {f"{obligatory_fields}": "field cannot be empty"}
        return True, content

    for key in list_key:
        if not food_order[key]:
            empty_fields.append(key)
    if empty_fields:
        content = {f"{empty_fields}": "field cannot be empty"}
        return True, content

    if not isinstance(food_order['products'], list):
        content = {"products": "expected list with values"}
        return True, content
    for field in ['firstname', 'lastname', 'address']:
        if not isinstance(food_order[field], str):
            content = {f"{field}": "expected string"}
            return True, content

    try:
        if not phonenumbers.is_valid_number(phonenumbers.parse(food_order['phonenumber'])):
            content = {"phonenumber": "fail"}
            return True, content
    except NumberParseException:
        content = {"phonenumber": "fail"}
        return True, content

    for prod in food_order['products']:
        if prod['product'] > product_amount or not isinstance(prod['product'], int):
            content = {"products": f"Invalid primary key - {prod['product']}"}
            return True, content

    return False, None


@api_view(['POST'])
def register_order(request):
    try:
        food_order = request.data
    except ValueError as error:
        return JsonResponse({
            "Error": error
        })

    is_f, content = check_fields(food_order)
    if is_f:
        return Response(content, status=status.HTTP_400_BAD_REQUEST)

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
    print(food_order['products'])
    content = {"fields_all": "ok"}
    return Response(content, status=status.HTTP_200_OK)

    # return JsonResponse({})
