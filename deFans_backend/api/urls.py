from django.urls import path
from .views import ( 
    CreatorView,
    AccountView, 
    CreatorPostView, 
    PostByCreatorView,
    CreateCreatorView,
    CreateAccountView,
    CreateCreatorPostView,
    LoginCreatorView,
    AddSubscriptionView,
    HomeScreen
)


urlpatterns = [
    path('creators/', CreatorView.as_view(), name='all-creators'),
    path('accounts/', AccountView.as_view(), name='all-accounts'),
    path('posts/', CreatorPostView.as_view(), name='all-posts'),
    path('posts/<int:user_id>/', PostByCreatorView.as_view(), name='user-posts'),
    path('signup_creator/', CreateCreatorView.as_view(), name='create-creator'),
    path('signup_account/', CreateAccountView.as_view(), name='create-Account'),
    path('login_creator/', LoginCreatorView.as_view(), name='login-creator'),
    path('create_post/', CreateCreatorPostView.as_view(), name='create-Post'),
    path('add-subscription/', AddSubscriptionView.as_view(), name='add-subscription'),
    path('home/', HomeScreen.as_view(), name='Home')
]
