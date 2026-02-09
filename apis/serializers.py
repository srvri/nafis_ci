#apis/serializers.py
from rest_framework import serializers
from nafis.models import Category, Size, Material, Apparel, ApparelImage, SlideShow, Contact, CartItem
from django.contrib.auth.models import User
from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class SizeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Size
        fields = '__all__'

class MaterialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Material
        fields = '__all__'

class ApparelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Apparel
        fields = '__all__'

class ApparelImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ApparelImage
        fields = '__all__'

class SlideShowSerializer(serializers.ModelSerializer):
    class Meta:
        model = SlideShow
        fields = '__all__'

class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = '__all__'

class CartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = '__all__'
