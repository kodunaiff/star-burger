from rest_framework import serializers

from .models import Order, OrderElements


class OrderElementsSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderElements
        fields = ["product", "quantity"]


class OrderSerializer(serializers.ModelSerializer):
    products = OrderElementsSerializer(many=True, write_only=True, allow_empty=False)

    class Meta:
        model = Order
        fields = ["id", "firstname", "lastname", "phonenumber", "address", "products"]

    def create(self, validated_data):
        order = Order.objects.create(
            firstname=validated_data['firstname'],
            lastname=validated_data['lastname'],
            phonenumber=validated_data['phonenumber'],
            address=validated_data['address'],
        )

        product_fields = validated_data['products']
        products = [OrderElements(
            order=order,
            position_cost=fields['product'].price * fields['quantity'],
            **fields) for fields in product_fields
        ]
        OrderElements.objects.bulk_create(products)

        return order
