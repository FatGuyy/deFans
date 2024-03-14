from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from rest_framework.permissions import AllowAny
from rest_framework.generics import ListAPIView, CreateAPIView

from .models import Creator, Account, CreatorPost
from .serializers import CreatorListSerializer, AccountListSerializer, CreatorPostListSerializer
    

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
    serializer_class = CreatorPostListSerializer

    def get_queryset(self):
        return CreatorPost.objects.all()

    def list(self, request):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class PostByCreatorView(ListAPIView):

    renderer_classes = [JSONRenderer]
    permission_classes = [AllowAny]
    serializer_class = CreatorPostListSerializer

    def get_queryset(self):
        """
        this gets the `user_id` in the URL
        """
        queryset = CreatorPost.objects.all()
        user = self.kwargs['user_id']
        if user is not None:
            queryset = queryset.filter(uploader__id=user)
        return queryset
    
    def list(self, request):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class CreateCreatorView(CreateAPIView):
    pass


class CreateAccountView(CreateAPIView):
    pass


class CreatePostView(CreateAPIView):
    pass
