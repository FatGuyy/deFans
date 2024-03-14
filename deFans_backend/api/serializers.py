from rest_framework import serializers
from .models import Creator, Account, CreatorPost

class CreatorListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Creator
        fields = ["user", "nickName", "bio", "price", "walletAddress"]

class AccountListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ["user", "nickName", "bio", "walletAddress"]

class CreatorPostListSerializer(serializers.ModelSerializer):
    class Meta:
        model = CreatorPost
        fields = ["uploader", "upload_date", "caption"]
