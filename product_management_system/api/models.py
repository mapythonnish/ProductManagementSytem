import random
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models

# Custom User model with role-based permissions
class User(AbstractUser):
    ROLE_CHOICES = [
        (1, 'Admin User'),
        (2, 'Product Manager'),
        (3, 'Product Creator'),
    ]
    role = models.PositiveSmallIntegerField(choices=ROLE_CHOICES, default=3)
    otp = models.CharField(max_length=6, blank=True, null=True)  # OTP field


    ADMIN_USER = 1  # Constant for Admin User
    PRODUCT_MANAGER = 2  # Constant for Product Manager
    PRODUCT_CREATOR = 3  # Constant for Product Creator

    # Method to generate OTP
    def generate_otp(self):
        self.otp = str(random.randint(100000, 999999))  # Generate a 6-digit OTP
        self.save()

    # Override groups and user_permissions fields to avoid conflicts
    groups = models.ManyToManyField(
        Group,
        related_name='custom_user_set',
        blank=True,
        help_text='The groups this user belongs to.',
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='custom_user_set',
        blank=True,
        help_text='Specific permissions for this user.',
    )

    # Meta class for custom behavior
    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    # String representation
    def __str__(self):
        return self.username



# Product model
class Product(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    fabric_type = models.CharField(max_length=100)
    description = models.TextField()
    published = models.BooleanField(default=False)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

# ProductColor model to represent different colors for the same product
class ProductColor(models.Model):
    product = models.ForeignKey(Product, related_name='colors', on_delete=models.CASCADE)
    color = models.CharField(max_length=50)
    sizes = models.CharField(max_length=50, choices=[('XS', 'XS'), ('S', 'S'), ('M', 'M'), ('L', 'L'), ('XL', 'XL')])

    def __str__(self):
        return f"{self.product.name} - {self.color}"