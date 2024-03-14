from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
# from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import ListAPIView

from .models import Creator, Account, CreatorPost
from .serializers import CreatorListSerializer, AccountListSerializer


class Check(APIView):
    renderer_classes = [JSONRenderer]

    def get(self, request):
        return Response({"hello":"world"})
    

class CreatorView(ListAPIView):

    renderer_classes = [JSONRenderer]
    permission_classes = [AllowAny]
    serializer_class = CreatorListSerializer

    def get_queryset(self):
        return Creator.objects.all()

    def list(self, request):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class AccountView(ListAPIView):

    renderer_classes = [JSONRenderer]
    permission_classes = [AllowAny]
    serializer_class = AccountListSerializer

    def get_queryset(self):
        return Account.objects.all()

    def list(self, request):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class CreatorPostView(ListAPIView):

    renderer_classes = [JSONRenderer]
    permission_classes = [AllowAny]
    serializer_class = None

    def get_queryset(self):
        return CreatorPost.objects.all()

    def list(self, request):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
