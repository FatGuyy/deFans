from rest_framework import status
from rest_framework.parsers import MultiPartParser, JSONParser
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.generics import ListAPIView, CreateAPIView
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.authentication import SessionAuthentication, TokenAuthentication

from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404

from .models import Creator, Account, CreatorPost
from .serializers import (
    CreatorSerializerList, 
    AccountSerializer, 
    CreatorPostSerializer, 
    CreateCreatorSerializer, 
    LoginCreatorSerializer,
    CreateAccountSerializer,
    UserSerializer
)


# get all the creators
class CreatorView(ListAPIView):

    renderer_classes = [JSONRenderer]
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

    renderer_classes = [JSONRenderer]
    # authentication_classes = []
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

    renderer_classes = [JSONRenderer]
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

    renderer_classes = [JSONRenderer]
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
    
    parser_classes = [MultiPartParser, JSONParser]
    renderer_classes = [JSONRenderer]
    permission_classes = [AllowAny]

    def post(self, request):
        creator = None
        serializer = CreateCreatorSerializer(data=request.data)
        if serializer.is_valid():
            user_data = serializer.validated_data.pop('user')
            user = User.objects.create_user(**user_data)
            token = Token.objects.create(user=user)
            try:
                with transaction.atomic():
                    creator = Creator.objects.create(user=user, **serializer.validated_data)
            except Exception as e:
                print("exception occured - ", e)
                user.delete()
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({"token": token.key, "user": CreateAccountSerializer(creator).data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Make a User
class CreateAccountView(CreateAPIView):
    
    parser_classes = [MultiPartParser, JSONParser]
    renderer_classes = [JSONRenderer]
    permission_classes = [AllowAny]

    def post(self, request):
        account = None
        serializer = CreateAccountSerializer(data=request.data)
        if serializer.is_valid():
            user_data = serializer.validated_data.pop('user')
            user = User.objects.create_user(**user_data)
            try:
                with transaction.atomic():
                    account = Account.objects.create(user=user, **serializer.validated_data)
            except Exception as e:
                print("exception occured - ", e)
                user.delete()
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response(CreateAccountSerializer(account).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CreatePostView(CreateAPIView):
    pass

# simple login view for a creator account
class LoginCreatorView(APIView):

    renderer_classes = [JSONRenderer]
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    parser_classes = [MultiPartParser, JSONParser]
    permission_classes = [IsAuthenticated]
    serializer_class = LoginCreatorSerializer

    def post(self, request):
        user = get_object_or_404(User, username=request.data['username'])
        if not user.check_password(request.data['password']):
            return Response({"Error":"credentials do not match"}, status=status.HTTP_404_NOT_FOUND)
        token, _ = Token.objects.get_or_create(user=user)
        serializer = UserSerializer(instance=user)
        return Response({"token":token.key, "user": serializer.data, "header_user": str(request.user)}, status=status.HTTP_200_OK)