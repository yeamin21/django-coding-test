from dataclasses import fields

from rest_framework import serializers

from .models import Product, ProductVariant, ProductVariantPrice, Variant


class ProductVariantSerializer(serializers.ModelSerializer):
    variant_title = serializers.CharField(allow_blank=True,required=False)
    variant = serializers.PrimaryKeyRelatedField(queryset=Variant.objects.all(), required=False)
    class Meta:
        model = ProductVariant
        fields=['variant_title','variant']
       

class VariantSerializer(serializers.ModelSerializer):
    # productvariant_set = ProductVariantSerializer(many=True)
    class Meta:
        model = Variant
        exclude = ['created_at','updated_at',]

    def to_representation(self, instance):
        data=super().to_representation(instance)
        data['productvariants'] = ProductVariantSerializer(instance.productvariant_set.values('variant_title').distinct(), many=True).data
        return data
class ProductVariantPriceSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    product_variant_one = ProductVariantSerializer(required=False)    
    product_variant_two = ProductVariantSerializer(required=False)
    product_variant_three = ProductVariantSerializer(required=False)
    class Meta:
        model = ProductVariantPrice
        exclude = ['created_at','updated_at','product']
   
class ProductSerializer(serializers.ModelSerializer):
    productvariant_set =ProductVariantSerializer( many=True)
    productvariantprice_set = ProductVariantPriceSerializer(many=True)
    class Meta: 
        model = Product
        fields = '__all__'

    def create(self, validated_data):
        product_variations_data = validated_data.pop('productvariant_set')
        product_variant_prices = validated_data.pop('productvariantprice_set')
        product = Product.objects.create(**validated_data)
          
        product_variations = [ProductVariant(product=product,**variant) for variant in product_variations_data]
        ProductVariant.objects.bulk_create(product_variations)
        product_variant_prices_set = []
        for i in product_variant_prices:
            prod_var={}
            try:
                if i['product_variant_one']['variant_title'] !='': 
                    prod_var['product_variant_one']=ProductVariant.objects.get(variant_title=i['product_variant_one']['variant_title'],product=product)
                if i['product_variant_two']['variant_title']!='':
                    prod_var['product_variant_two']= ProductVariant.objects.get(variant_title=i['product_variant_two']['variant_title'],product=product)
                if i['product_variant_three']['variant_title']!='':
                    prod_var['product_variant_three']=ProductVariant.objects.get(variant_title=i['product_variant_three']['variant_title'],product=product)
            except:
                pass
            finally:
                prod_var['price']=i['price']
                prod_var['stock']=i['stock']
            product_variant_prices_set.append(ProductVariantPrice(product=product,**prod_var))
        ProductVariantPrice.objects.bulk_create(product_variant_prices_set)
        return product
    def update(self, instance, validated_data):
        
        product_variations_data = validated_data.pop('productvariant_set')
        product_variant_prices = validated_data.pop('productvariantprice_set')
        for product_variant_price in product_variant_prices:
            product_var_price= ProductVariantPrice.objects.get(id=product_variant_price['id'])
            # product_variant_price['product']=instance
            product_var_price.price=product_variant_price['price']
            product_var_price.stock=product_variant_price['stock']
            product_var_price.save()
            
        instance.title = validated_data.get('title', instance.title)
        instance.sku = validated_data.get('sku', instance.sku)
        instance.description = validated_data.get('description', instance.description)  
        instance.save()
        return instance
        # return super().update(instance, validated_data)
