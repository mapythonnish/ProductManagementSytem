from django.urls import path, include
from .views import LoginView, VerifyOTPView, SignupView
from .views import PublishProductView, ProductListCreateView, ProductDetailView, BulkUploadProductView


 

urlpatterns = [
    # Auth-related routes
    path('signup/', SignupView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),
    path('verify-otp/', VerifyOTPView.as_view(), name='verify_otp'),
    
    path('products/', ProductListCreateView.as_view(), name='product-list-create'),
    path('products/<int:pk>/', ProductDetailView.as_view(), name='product-detail'),
    path('products/<int:pk>/publish/', PublishProductView.as_view(), name='publish-product'),
    path('products/bulk-upload/', BulkUploadProductView.as_view(), name='bulk-upload-product'),
]
