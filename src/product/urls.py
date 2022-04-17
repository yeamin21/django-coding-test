from django.urls import path
from django.views.generic import TemplateView

from product.views.product import (CreateProductView, ListProductView,
                                   ProductUpdateView)
from product.views.variant import (VariantCreateView, VariantEditView,
                                   VariantView)

app_name = "product"

urlpatterns = [
    # Variants URLs
    path('variants/', VariantView.as_view(), name='variants'),
    path('variant/create', VariantCreateView.as_view(), name='create.variant'),
    path('variant/<int:id>/edit', VariantEditView.as_view(), name='update.variant'),

    # Products URLs
    path('create/', CreateProductView.as_view(), name='create.product'),
    path('list/', ListProductView.as_view(), name='list.product'),
    path('<int:pk>/update/',ProductUpdateView.as_view())
]
