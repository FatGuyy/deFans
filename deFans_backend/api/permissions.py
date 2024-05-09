# from rest_framework.permissions import BasePermission

# # user.has_perm("appName.verb_modelName")

# class IsCreator(BasePermission):
#     message = 'Only creators are allowed to perform this action.'

#     def has_permission(self, request, view):
#         return request.user.is_authenticated and request.user.is_creator()
