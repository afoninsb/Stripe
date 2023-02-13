from django.urls import path

from product.views import (
    GetSessionIdView,
    ProductPageView,
    SuccessView,
    CancelView,
    PutToOrderView,
    ProductListView,
    OrderPageView,
    GetSessionIdForOrderView
)

app_name = 'product'

urlpatterns = [
    path(
        'buy/<pk>/',
        GetSessionIdView.as_view(),
        name='get_session_id'
    ),
    path(
        'buy/',
        GetSessionIdForOrderView.as_view(),
        name='get_session_id_order'
    ),
    path(
        'item/<pk>/',
        ProductPageView.as_view(),
        name='buy_item'
    ),
    path(
        'order/',
        OrderPageView.as_view(),
        name='order'
    ),
    path(
        'to_order/',
        PutToOrderView.as_view(),
        name='to_order'
    ),
    path('cancel/', CancelView.as_view(), name='cancel'),
    path('success/', SuccessView.as_view(), name='success'),
    path(
        '',
        ProductListView.as_view(),
        name='product_list'
    ),
]
