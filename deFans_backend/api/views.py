from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.generics import ListAPIView, CreateAPIView
from rest_framework.authtoken.models import Token
# from rest_framework.decorators import authentication_classes, permission_classes
# from rest_framework.authentication import SessionAuthentication, TokenAuthentication

from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import Group
from django.db import transaction
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404

from .models import Creator, Account, CreatorPost, Subscription
from .utilis import createWallet
from .serializers import (
    CreatorSerializerList, 
    AccountSerializer, 
    CreatorPostSerializer, 
    CreateCreatorSerializer, 
    LoginUserSerializer,
    CreateAccountSerializer,
    CreateCreatorPostSerializer,
    AddSubscription
)


# get all the creators
class CreatorView(ListAPIView):

    permission_classes = [AllowAny] # empty means anyone can access the class
    serializer_class = CreatorSerializerList

    def get_queryset(self):
        return Creator.objects.all()

    def list(self, request):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


# get all the Accounts
class AccountView(ListAPIView):

    permission_classes = [AllowAny]
    serializer_class = AccountSerializer

    def get_queryset(self):
        return Account.objects.all()

    def list(self, request):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


# get all the creators' Posts
class CreatorPostView(ListAPIView):

    permission_classes = [AllowAny]
    serializer_class = CreatorPostSerializer

    def get_queryset(self):
        return CreatorPost.objects.all()

    def list(self, request):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


# Get all the Creator's Posts by user_id
class PostByCreatorView(ListAPIView):

    permission_classes = [AllowAny]
    serializer_class = CreatorPostSerializer

    def get_queryset(self):
        """
        this gets the `user_id` in the URL
        """
        queryset = CreatorPost.objects.all()
        user = self.kwargs['user_id']
        if user is not None:
            try:
                queryset = queryset.filter(uploader__id=user)
            except ObjectDoesNotExist:
                queryset = CreatorPost.objects.none()
        return queryset
    
    def list(self, request):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


# Make a Creator
class CreateCreatorView(CreateAPIView):
    
    permission_classes = [AllowAny]

    def post(self, request):
        creator = None
        request.data["nickName"] = request.data['user']['username']
        serializer = CreateCreatorSerializer(data=request.data)
        wallet, mnemonic = createWallet()
        if serializer.is_valid():
            user_data = serializer.validated_data.pop('user')
            user = User.objects.create_user(**user_data)
            # Adding user in the Creator group
            my_group = Group.objects.get(name='Creator') 
            my_group.user_set.add(user)
            # generating a token for the user
            token = Token.objects.create(user=user)
            try:
                serializer.validated_data['walletAddress'] = wallet.address
                with transaction.atomic():
                    creator = Creator.objects.create(user=user, **serializer.validated_data)
            except Exception as e:
                print("exception occured - ", e)
                user.delete()
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({"token": token.key, "Creator": CreateCreatorSerializer(creator).data, "mnemonic": str(mnemonic)}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Make a Account
class CreateAccountView(CreateAPIView):
    
    permission_classes = [AllowAny]

    def post(self, request):
        account = None
        request.data["nickName"] = request.data['user']['username']
        serializer = CreateAccountSerializer(data=request.data)
        wallet, mnemonic = createWallet()
        if serializer.is_valid():
            user_data = serializer.validated_data.pop('user')
            user = User.objects.create_user(**user_data)
            my_group = Group.objects.get(name='Account') 
            my_group.user_set.add(user)
            token = Token.objects.create(user=user)
            try:
                serializer.validated_data['walletAddress'] = wallet.address
                with transaction.atomic():
                    account = Account.objects.create(user=user, **serializer.validated_data)
                    print("subscriptions - ", account.subscriptions)
                    account.subscriptions.clear()
            except Exception as e:
                print("exception occured - ", e)
                user.delete()
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({"token": token.key, "account": CreateAccountSerializer(account).data, "mnemonic": str(mnemonic)}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Create a Creator Post
class CreateCreatorPostView(CreateAPIView):
    
    serializer_class = CreateCreatorPostSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = CreateCreatorPostSerializer(data=request.data)
        if serializer.is_valid():
            try:
                with transaction.atomic():
                    user=request.user
                    uploader=Creator.objects.get(user=user)
                    post = CreatorPost.objects.create(uploader=uploader, **serializer.validated_data)
                    return Response({"post": CreateCreatorPostSerializer(post).data}, status=status.HTTP_201_CREATED)
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# simple login view for a creator account
class LoginCreatorView(ListAPIView):

    permission_classes = [AllowAny]
    serializer_class = LoginUserSerializer

    def post(self, request):
        user = get_object_or_404(User, email=request.data['email'])
        if not user.check_password(request.data['password']):
            return Response({"Error":"credentials do not match"}, status=status.HTTP_404_NOT_FOUND)
        token, _ = Token.objects.get_or_create(user=user)
        # serializer = UserSerializer(instance=user)
        return Response({"token":token.key, "header_user": str(request.user)}, status=status.HTTP_200_OK)


# View to Login Account
class LoginAccount(ListAPIView):

    permission_classes = [AllowAny]
    serializer_class = LoginUserSerializer

    def post(self, request):
        user = get_object_or_404(User, email=request.data['email'])
        if not user.check_password(request.data['password']):
            return Response({"Error":"credentials do not match"}, status=status.HTTP_404_NOT_FOUND)
        token, _ = Token.objects.get_or_create(user=user)
        return Response({"token":token.key, "header_user": str(request.user)}, status=status.HTTP_200_OK)


# View to Add a sub
class AddSubscriptionView(CreateAPIView):
    
    permission_classes = [AllowAny]
    serializer_class = AddSubscription

    def post(self, request):
        # getting ids from the username
        creator_user = User.objects.get(username=request.data['creator'])
        account_user = User.objects.get(username=request.data['account'])
        creator = Creator.objects.get(user=creator_user)
        account = Account.objects.get(user=account_user)
        creator = creator.id
        account = account.id

        serializer = AddSubscription(data={"creator":creator, "account":account})
        # Have to check if the Subscription already exists...
        if serializer.is_valid():
            subscription = serializer.save()  # Create the subscription
            return Response({
                "message": "Subscription created successfully",
                "subscription": str(subscription)
            }, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# View to get posts as per an account
class HomeScreen(ListAPIView):

    serializer_class = CreateCreatorPostSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self, request):
        user = request.user
        account = Account.objects.get(user=user)

        # This represents all the subscription the user has
        subscription_list = Subscription.objects.filter(account=account).values_list('creator', flat=True)
        return list(subscription_list)

    def posts_from_a_creator(self, id:int):
        creator = None
        # creator= Creator.objects.get(id=id)
        try:
            creator = Creator.objects.get(id=id)
        except ObjectDoesNotExist:
            return None
        print("creator - ", creator)
        posts = CreatorPost.objects.filter(uploader=creator)
        return list(set(posts))

    def post(self, request):
        # this is returning some account type user - find out why?
        query = self.get_queryset(request=request)
        print("query - ", query)
        if query is None:
            return Response({"error":"No subsription"}, status=status.HTTP_403_FORBIDDEN)
        
        posts_list = []
        for creator_id in query:
            posts_list.append(self.posts_from_a_creator(creator_id))
        for posts in posts_list:
            for post in posts:
                print(post.content)
        print("posts list - ", posts_list)
        return Response({"query":str(posts_list)}, status=status.HTTP_200_OK)


# View to 