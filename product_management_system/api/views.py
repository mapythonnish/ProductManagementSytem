from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import UserSignupSerializer
from rest_framework.permissions import AllowAny
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from .models import Product, ProductColor, User
from .serializers import ProductSerializer, UserSignupSerializer
from .permissions import  IsAdmin
import pandas as pd

class SignupView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserSignupSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'User registered successfully!'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

from django.core.mail import send_mail
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .models import User

class LoginView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        # Authenticate the user
        user = authenticate(username=username, password=password)

        if user:
            # Generate OTP
            user.generate_otp()

            # Send OTP via email
            send_mail(
                'Your Login OTP',
                f'Your OTP is: {user.otp}',
                'yourapp@example.com',  # Replace with your email
                [user.email],
                fail_silently=False,
            )

            return Response({'message': 'OTP sent to your email.'}, status=status.HTTP_200_OK)
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

class VerifyOTPView(APIView):
    def post(self, request):
        username = request.data.get('username')
        otp = request.data.get('otp')

        try:
            user = User.objects.get(username=username, otp=otp)
            # Clear the OTP after successful verification
            user.otp = None
            user.save()

            # Generate tokens
            refresh = RefreshToken.for_user(user)

            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({'error': 'Invalid OTP'}, status=status.HTTP_400_BAD_REQUEST)


 

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import Product, ProductColor
from .serializers import ProductSerializer
from .permissions import IsAdminOrProductManager, IsOwnerOrAdmin,IsProductCreator
import pandas as pd

class ProductListCreateView(APIView):
    """
    Handle listing all products and creating a new product
    """
    permission_classes = [IsAuthenticated, IsAdminOrProductManager]

    def get(self, request):
        # Allow only GET requests to list products
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        # Allow only POST requests to create a new product
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            # Save the product, associating it with the logged-in user
            serializer.save(created_by=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProductDetailView(APIView):
    """
    Handle retrieving, updating, and deleting a product
    """
    permission_classes = [IsAuthenticated, IsAdminOrProductManager]

    def get(self, request, pk):
        try:
            product = Product.objects.get(pk=pk)
            serializer = ProductSerializer(product)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Product.DoesNotExist:
            return Response({"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, pk):
        try:
            product = Product.objects.get(pk=pk)
            self.check_object_permissions(request, product)  # Ensures only owner or admin can update
            serializer = ProductSerializer(product, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Product.DoesNotExist:
            return Response({"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk):
        try:
            product = Product.objects.get(pk=pk)
            self.check_object_permissions(request, product)  # Ensures only owner or admin can delete
            product.delete()
            return Response({"message": "Product deleted successfully!"}, status=status.HTTP_204_NO_CONTENT)
        except Product.DoesNotExist:
            return Response({"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND)


class PublishProductView(APIView):
    """
    Admin can publish/unpublish a product
    """
    permission_classes = [IsAuthenticated, IsAdmin]

    def post(self, request, pk):
        try:
            product = Product.objects.get(pk=pk)
            product.published = not product.published
            product.save()
            return Response({"message": "Product published/unpublished successfully!"}, status=status.HTTP_200_OK)
        except Product.DoesNotExist:
            return Response({"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND)


class BulkUploadProductView(APIView):
    """
    Upload products in bulk from an Excel file
    """
    permission_classes = [IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request):
        file = request.FILES.get('file')
        if not file:
            return Response({"error": "No file uploaded"}, status=status.HTTP_400_BAD_REQUEST)

        data = pd.read_excel(file)

        for _, row in data.iterrows():
            product = Product.objects.create(
                name=row['Product Name'],
                price=row['Product Price'],
                discount_price=row['Discount Price'],
                fabric_type=row['Fabric Type'],
                description=row['Product Description'],
                created_by=request.user
            )
            colors = row['Color'].split(",")  # Assuming colors are comma separated in the Excel
            for color in colors:
                ProductColor.objects.create(
                    product=product,
                    color=color.strip(),
                    sizes=row['Size']  # Assuming size field exists in Excel
                )

        return Response({"message": "Products uploaded successfully!"}, status=status.HTTP_201_CREATED)
