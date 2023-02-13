import contextlib
import stripe

from django.db.models import Exists, OuterRef

from product.models import Discount, Item, Order


def get_items():
    items = Item.objects.filter(Exists(
        Order.objects.filter(item=OuterRef('id'))
        )).select_related('tax')
    return (
        [
            {
                'price_data': {
                    'currency': item.currency,
                    'unit_amount': item.price,
                    'product_data': {'name': item.name},
                },
                'quantity': 1,
                'tax_rates': get_tax(item.tax),
            }
            for item in items
        ]
        if items
        else None
    )


def get_coupon(request):
    if discount := request.GET.get('discount', ''):
        if coupon := Discount.objects.filter(id=discount):
            with contextlib.suppress(Exception):
                stripe.Coupon.create(
                    id=coupon[0].id,
                    percent_off=coupon[0].percent_off
                )
            return [{'coupon': coupon[0].id}]
    return None


def get_tax(tax):
    if not tax:
        return None
    if tax_id := next(
        (
            tax_item['id']
            for tax_item in stripe.TaxRate.list(limit=3)['data']
            if tax_item['display_name'] == tax.display_name
        ),
        '',
    ):
        return [tax_id]
    with contextlib.suppress(Exception):
        create_tax = stripe.TaxRate.create(
            display_name=tax.display_name,
            inclusive=tax.inclusive,
            percentage=tax.percentage,
        )
    return [create_tax.id]


def get_intent():
    items = Item.objects.filter(Exists(
        Order.objects.filter(item=OuterRef('id'))
        )).select_related('tax')
    return stripe.PaymentIntent.create(
        amount=items[0].price,
        currency=items[0].currency,
        payment_method_types=['card'],
    )
