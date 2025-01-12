from rest_framework import serializers
from .models import User

class UserSignupSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password', 'email', 'role']

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            email=validated_data['email'],
            role=validated_data['role']
        )
        return user
    
from rest_framework import serializers
from .models import Product, ProductColor, User

class ProductColorSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductColor
        fields = ['color', 'sizes']

from rest_framework import serializers
from .models import Product, ProductColor

class ProductColorSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductColor
        fields = ['color', 'sizes']

class ProductSerializer(serializers.ModelSerializer):
    colors = ProductColorSerializer(many=True)  # Expecting a list of colors

    class Meta:
        model = Product
        fields = ['name', 'price', 'discount_price', 'fabric_type', 'description', 'published', 'colors']

    def create(self, validated_data):
        colors_data = validated_data.pop('colors', [])
        product = Product.objects.create(**validated_data)
        
        # Create product color objects
        for color_data in colors_data:
            ProductColor.objects.create(product=product, **color_data)
        
        return product

    def update(self, instance, validated_data):
        colors_data = validated_data.pop('colors', [])
        # Update product instance
        instance.name = validated_data.get('name', instance.name)
        instance.price = validated_data.get('price', instance.price)
        instance.discount_price = validated_data.get('discount_price', instance.discount_price)
        instance.fabric_type = validated_data.get('fabric_type', instance.fabric_type)
        instance.description = validated_data.get('description', instance.description)
        instance.published = validated_data.get('published', instance.published)
        instance.save()
        
        # Delete existing color entries
        instance.colors.all().delete()
        
        # Add new colors
        for color_data in colors_data:
            ProductColor.objects.create(product=instance, **color_data)
        
        return instance
