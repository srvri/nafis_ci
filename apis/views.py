#apis/views.py
from rest_framework import viewsets
from nafis.models import Category,Size, Material, Apparel, ApparelImage, SlideShow, Contact, CartItem
from .serializers import (
    CategorySerializer, SizeSerializer,
    MaterialSerializer, ApparelSerializer, ApparelImageSerializer,
    SlideShowSerializer, ContactSerializer, CartItemSerializer
)
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.decorators import action
from django.contrib.auth.models import User
from .serializers import UserSerializer
from dj_rest_auth.views import LoginView, LogoutView

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def me(self, request):
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class SizeViewSet(viewsets.ModelViewSet):
    queryset = Size.objects.all()
    serializer_class = SizeSerializer

class MaterialViewSet(viewsets.ModelViewSet):
    queryset = Material.objects.all()
    serializer_class = MaterialSerializer

class ApparelViewSet(viewsets.ModelViewSet):
    queryset = Apparel.objects.all()
    serializer_class = ApparelSerializer

class ApparelImageViewSet(viewsets.ModelViewSet):
    queryset = ApparelImage.objects.all()
    serializer_class = ApparelImageSerializer

class SlideShowViewSet(viewsets.ModelViewSet):
    queryset = SlideShow.objects.all()
    serializer_class = SlideShowSerializer

class ContactViewSet(viewsets.ModelViewSet):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer

class CartItemViewSet(viewsets.ModelViewSet):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer
