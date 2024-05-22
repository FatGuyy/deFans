from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import CreateAPIView

from django.contrib.auth.models import User
import requests

from .models import Chat
from api.models import Creator, Account, Subscription
from .serializers import ChatSerializer, ChatMessageSerializer

class CreateChatView(CreateAPIView):

    permission_classes = [IsAuthenticated]
    serializer_class = ChatSerializer

    def post(self, request):
        user = request.user
        try:
            # check if user is Account
            sender = Account.objects.get(user=user)
            

            # check all the subscription the account has
            subscription_list = list(Subscription.objects.filter(account=sender).values_list('creator', flat=True))
            subscription_list = [Creator.objects.get(id=x) for x in subscription_list]
            
            # gettiing the account object using username
            request.data['creator'] = Creator.objects.get(user=User.objects.get(username=request.data.get('creator')))
            if request.data['creator'] in subscription_list:
                serializer = ChatSerializer(data=request.data)
                request.data['account'] = sender.id
                request.data['creator'] = request.data['creator'].id
                if serializer.is_valid():
                    chat = Chat.objects.create(**serializer.validated_data)
                    return Response({"chat":ChatSerializer(chat).data}, status=status.HTTP_200_OK)
                else:
                    return Response({"error":serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({"error":"You dont have the required subscription", 
                                 "available": str(subscription_list)}, status=status.HTTP_400_BAD_REQUEST)

        except:
            # if user is Creator
            try:
                sender = Creator.objects.get(user=user)
            except:
                return Response({"error":"bad token"})

            # check all the subscription the creator has
            subscription_list = Subscription.objects.filter(creator=sender).values_list('account', flat=True)
            subscription_list = [Account.objects.get(id=x) for x in subscription_list]
            
            # gettiing the account object using username
            request.data['account'] = Account.objects.get(user=User.objects.get(username=request.data['account']))
            if request.data['account'] in subscription_list:
                serializer = ChatSerializer(data=request.data)
                request.data['creator'] = sender.id
                request.data['account'] = request.data['account'].id
                if serializer.is_valid():
                    chat = Chat.objects.create(**serializer.validated_data)
                    return Response({"chat":ChatSerializer(chat).data}, status=status.HTTP_200_OK)
                else:
                    return Response({"error":serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({"error":"You dont have the required subscription", 
                                 "available": str(subscription_list)}, status=status.HTTP_400_BAD_REQUEST)


class CreateMessageView(CreateAPIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):
        sender = request.user
        chats = Chat.objects.filter(account=(Account.objects.get(user=User.objects.get(username=str(sender)))).id)
        receiver = Creator.objects.get(user=User.objects.get(username=request.data['receiver']))
        
        # Check if the receiver already has a chat, else try to create one
        available = [chat.creator for chat in chats]
        if receiver in available:
            index = available.index(receiver)
            print("creators - ", available)
            print("receiver id -", receiver.id)
        # Meaning the chat is not present, 
        else:
            index = 1
            print("there is no chat")
            create = CreateChatView()
            request.method = 'POST'

            # Making the json for request based on the type of the sender
            if Account.objects.get(user=sender):
                url = 'http://127.0.0.1:8000/chats/create_chat'
                headers = {
                    'Authorization': 'Token dd760e7fab612ed4da051e4b36aeb943fd8bab13',
                    'Content-Type': 'application/json'
                }
                data = {
                    "creator": "_girl",
                    "account": ""
                }
                response = requests.post(url, json=data, headers=headers)

                print(f"Status Code: {response.status_code}")
                print(f"Response JSON: {response.json()}")
                print("res header - ", response.headers)
            else:
                request.user = sender
                request.data['account'] = str(receiver)
                request.data['creator'] = str(sender.username)
                print(request.data)
                print('sender is creator type of user')
            request.META['HTTP_HOST'] = 'http://127.0.0.1:8000/chats/create_chat'
            create.post(request=request)

        request.data['chat'] = chats[index-1].id
        request.data['sender'] = sender.id
        request.data['receiver'] = receiver.user.id
        serializer = ChatMessageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"Message": str(serializer.validated_data)}, status=status.HTTP_200_OK)
        else:
            return Response({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
