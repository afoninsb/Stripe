import stripe

from django.conf import settings
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.views import View
from django.views.generic import TemplateView

from product.functions import get_coupon, get_intent, get_items
from product.models import Item, Order

stripe.api_key = settings.STRIPE_SECRET_KEY


# ОСНОВНОЕ ЗАДАНИЕ

class GetSessionIdView(View):
    """Получаем Stripe Session Id для оплаты выбранного Item."""

    def get(self, request, *args, **kwargs):
        product_id = self.kwargs.get('pk')
        product = Item.objects.get(id=product_id)
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[
                {
                    'price_data': {
                        'currency': 'RUB',
                        'unit_amount': product.price,
                        'product_data': {'name': product.name},
                    },
                    'quantity': 1,
                },
            ],
            mode='payment',
            success_url=f'{settings.DOMAIN}/success/',
            cancel_url=f'{settings.DOMAIN}/cancel/',
        )
        # return redirect(checkout_session.url)
        return JsonResponse({
            'id': checkout_session.id
        })


class ProductPageView(TemplateView):
    """Страница товара."""

    template_name = "product.html"

    def get_context_data(self, **kwargs):
        product_id = self.kwargs.get('pk')
        product = Item.objects.get(id=product_id)
        context = super().get_context_data(**kwargs)
        context.update({
            "product": product,
        })
        return context


# ДОПОЛНИТЕЛЬНЫЕ ЗАДАНИЯ

class ProductListView(TemplateView):
    """Главная - список всех товаров."""

    template_name = "list.html"

    def get_context_data(self, **kwargs):
        products = Item.objects.all()
        context = super().get_context_data(**kwargs)
        context.update({
            "products": products,
        })
        return context


class PutToOrderView(View):
    """Сохраняем выбранные товары в Order."""

    def post(self, request):
        Order.objects.all().delete()
        ids = request.POST.getlist('id')
        bulk_data = [Order(
            item_id=ids[i],
        ) for i in range(len(ids))]
        Order.objects.bulk_create(bulk_data)
        return redirect('product:order')


class OrderPageView(TemplateView):
    """Страница товаров в Order."""

    template_name = "order.html"

    def get_context_data(self, **kwargs):
        order = Order.objects.all().select_related('item')
        context = super().get_context_data(**kwargs)
        context.update({
            "order": order,
        })
        return context


class GetSessionIdForOrderView(View):
    """Получаем Stripe Session Id для оплаты товаров в Order."""

    def get(self, request, *args, **kwargs):
        button_name = request.GET.get('button')
        if button_name == 'checkout.Session':
            try:
                checkout_session = stripe.checkout.Session.create(
                    payment_method_types=['card'],
                    line_items=get_items(),
                    discounts=get_coupon(request),
                    mode='payment',
                    success_url=f'{settings.DOMAIN}/success/',
                    cancel_url=f'{settings.DOMAIN}/cancel/',
                )
            except Exception:
                return HttpResponse(
                    'Товары в разных валютах. Оплатите по очереди')
            finally:
                Order.objects.all().delete()
            # return redirect(checkout_session.url)
            return JsonResponse({
                'id': checkout_session.id
            })
        intent = get_intent()
        return render(
            request,
            'checkout.html',
            {
                'client_secret': intent.client_secret,
                'api_key': settings.STRIPE_PUBLIC_KEY,
            }
        )


class SuccessView(TemplateView):
    template_name = "success.html"


class CancelView(TemplateView):
    template_name = "cancel.html"
