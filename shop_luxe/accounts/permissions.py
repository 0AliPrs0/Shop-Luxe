from rest_framework.permissions import BasePermission

class IsCustomerUser(BasePermission):
    def has_permission(self, request, view):
        return request.user.groups.filter(name='Customers').exists()

class IsSellerUser(BasePermission):
    def has_permission(self, request, view):
        return request.user.groups.filter(name='Sellers').exists()