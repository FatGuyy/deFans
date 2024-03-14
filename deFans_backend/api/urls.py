from django.urls import path
from .views import Check, CreatorView, AccountView


urlpatterns = [
    path('index/', Check.as_view()),
    path('creators/', CreatorView.as_view()),
    path('accounts/', AccountView.as_view()),
]
