from rest_framework import permissions
from .models import User

class IsAdminOrProductManager(permissions.BasePermission):
    """
    Custom permission for Admin or Product Manager role.
    """
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            # Admin (role=1) can perform all actions
            if request.user.role == User.ADMIN_USER:
                return True
            
            # Product Managers (role=2) can list, create, and update products
            if request.user.role == User.PRODUCT_MANAGER:
                if request.method in ['GET', 'POST', 'PUT']:  # Modify based on your need
                    return True
            
            # Product Creators (role=3) can create and list products
            if request.user.role == User.PRODUCT_CREATOR:
                if request.method in ['GET', 'POST']:
                    return True
        return False



class IsAdmin(permissions.BasePermission):
    """
    Custom permission for Admin role only
    """
    def has_permission(self, request, view):
        # Check if user is an Admin
        if request.user.role == User.ADMIN_USER:
            return True
        return False

class IsProductCreator(permissions.BasePermission):
    """
    Custom permission for Product Creator role
    """
    def has_permission(self, request, view):
        # Check if user is a Product Creator
        if request.user.role == User.PRODUCT_CREATOR:
            # Product Creators can only create or list products
            return view.action in ['create', 'list']
        return False


class IsOwnerOrAdmin(permissions.BasePermission):
    """
    Custom permission to check if the user is the owner of the product (or an admin)
    """
    def has_object_permission(self, request, view, obj):
        # Admin can access all products, otherwise, only the owner (creator) can update/delete
        if request.user.role == User.ADMIN_USER:
            return True
        return obj.created_by == request.user
