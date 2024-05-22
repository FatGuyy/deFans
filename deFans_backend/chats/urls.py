from django.urls import path
from .views import (
    CreateChatView,
    CreateMessageView
)


urlpatterns = [
    path('create_chat/', CreateChatView.as_view(), name='create-chat'),
    path('messsage/', CreateMessageView.as_view(), name='send-message')
]
