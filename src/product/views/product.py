from cmath import log
from operator import ge
from urllib import request
from webbrowser import get

from django.views import generic
from rest_framework import response, viewsets
from rest_framework.pagination import PageNumberPagination

from product.models import Product, Variant
from product.serializers import ProductSerializer


class ProductUpdateView(generic.UpdateView):
    model = Product
    fields = '__all__'
    template_name='products/update.html'
    context_object_name='product'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        variants = Variant.objects.filter(active=True).values('id', 'title')
        context['variants'] = list(variants.all())
        return context

class CustomPagination(PageNumberPagination):
    page_size = 2 
    page_size_query_param = 'page_size'
    def get_paginated_response(self, data):
        return response.Response({
            'start_index':self.page.start_index(),
            'end_index':self.page.end_index(),
            'page_size': self.page_size,
            'total_objects': self.page.paginator.count,
            'total_pages': self.page.paginator.num_pages,
            'current_page_number': self.page.number,
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'results': data,
        })

class CreateProductView(generic.TemplateView):
    template_name = 'products/create.html'

    def get_context_data(self, **kwargs):
        context = super(CreateProductView, self).get_context_data(**kwargs)
        variants = Variant.objects.filter(active=True).values('id', 'title')
        context['product'] = True
        context['variants'] = list(variants.all())
        return context

class ListProductView(generic.TemplateView):
    template_name = 'products/list.html'
    

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    pagination_class = CustomPagination

    def get_queryset(self):
        filter_string = {}
        if self.request.GET.get('title'): 
            filter_string['title__icontains']= self.request.GET.get('title')
        if self.request.GET.get('variant'):
            filter_string['productvariant__variant_title'] = self.request.GET.get('variant')
        if self.request.GET.get('price_from'):
            filter_string['productvariantprice__price__gte'] = self.request.GET.get('price_from')
        if self.request.GET.get('price_to'):
            filter_string['productvariantprice__price__lte'] = self.request.GET.get('price_to')
        if self.request.GET.get('date'):
            filter_string['created_at__date']=self.request.GET.get('date')
        print(filter_string)
        return super().get_queryset().filter(**filter_string)


    def create(self, request, *args, **kwargs):
        productvariants=[]
        for i in request.data.get('product_variant'):
            for j in i['tags']:
                productvariants.append({'variant':i['option'],'variant_title':j })
       
        productvariantprices = []
        nums=['one','two','three']
        for i in request.data.get('product_variant_prices'):
            product_variation_titles =  i['title'].split('/')
            product_variation_price={}

            for j in range(len(product_variation_titles)):
                product_variation_price['product_variant_'+nums[j]] = {'variant_title':product_variation_titles[j]}
              
            product_variation_price['price'] = i['price']
            product_variation_price['stock'] = i['stock']
            productvariantprices.append(product_variation_price)
        data = {
            'title': request.data.get('title'),
            'description': request.data.get('description'),
            'sku': request.data.get('sku'),
            'productvariant_set': productvariants,
            'productvariantprice_set': productvariantprices
        }
     
        serializer = self.get_serializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return response.Response(serializer.data, status=201)
            # serializer.save()
        else:
            return response.Response(serializer.errors, status=400)
      
    def update(self, request, *args, **kwargs):
        serializer = ProductSerializer(instance=self.get_object(),data=request.data)
        if serializer.is_valid():
           
            serializer.save()
        else:
            print(serializer.errors)
 
        # return super().update(request, *args, **kwargs)
