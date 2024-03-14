from django.urls import path
from .views import ( 
    CreatorView,
    AccountView, 
    CreatorPostView, 
    PostByCreatorView,
    CreateCreatorView,
    CreateAccountView,
    CreatePostView
)


urlpatterns = [
    path('creators/', CreatorView.as_view(), name='all-creators'),
    path('accounts/', AccountView.as_view(), name='all-accounts'),
    path('posts/', CreatorPostView.as_view(), name='all-posts'),
    path('posts/<int:user_id>/', PostByCreatorView.as_view(), name='user-posts'),
    path('create_creator/', CreateCreatorView.as_view(), name="create-creator"),
    path('create_account/', CreateAccountView.as_view(), name="create-Account"),
    path('create_post/', CreatePostView.as_view(), name="create-Post"),
]
