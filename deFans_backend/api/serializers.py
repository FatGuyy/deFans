from rest_framework import serializers
from .models import Creator, Account, CreatorPost, Subscription
from django.contrib.auth.models import User

# User serializer
class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['username', 'email', 'password']


# Serializer for creating a Creator
class CreateCreatorSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Creator
        fields = ['user', 'nickName', 'bio', 'price', 'walletAddress']

class CreateAccountSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Creator
        fields = ['user', 'nickName', 'bio', 'walletAddress']

class CreateCreatorPostSerializer(serializers.ModelSerializer):

    class Meta:
        model = CreatorPost
        fields = ["content", "caption"]

# Serializer for quering Creator
class CreatorSerializerList(serializers.ModelSerializer):

    class Meta:
        model = Creator
        fields = ["id", "user", "nickName", "bio", "price", "walletAddress"]


# Serializer for quering Account
class AccountSerializer(serializers.ModelSerializer):

    class Meta:
        model = Account
        fields = ["id", "user", "nickName", "bio", "walletAddress"]

# Serializer for quering CreatorPost
class CreatorPostSerializer(serializers.ModelSerializer):

    class Meta:
        model = CreatorPost
        fields = ["id", "uploader", "upload_date", "caption"]

# Serializer for Logging in Creator and Account
class LoginUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ["email", "password"]

class AddSubscription(serializers.ModelSerializer):
    # creator_username = serializers.CharField()
    # account_username = serializers.CharField()

    class Meta:
        model = Subscription
        fields = ["creator", "account"]

