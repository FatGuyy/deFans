from django.db import models
from django.contrib.auth.models import User

from api.models import Creator, Account


class Chat(models.Model):

    creator = models.ForeignKey(Creator, on_delete=models.CASCADE)
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"Chat between {self.creator.user.username} and {self.account.user.username}"
    
    def get_creator(self) -> str:
        return self.creator.user.username
    
    def get_account(self) -> str:
        return self.account.user.username

    class Meta:
        unique_together = ('creator', 'account')


class ChatMessage(models.Model):
    
    chat = models.ForeignKey(Chat, related_name='messages', on_delete=models.CASCADE)
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sender')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='receiver')
    content = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.content
    
    class Meta:
        ordering = ['sent_at']
