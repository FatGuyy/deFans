from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.core.validators import RegexValidator

# Need to remove the blank=True later, when we have other things implemented 
class Creator(models.Model):

    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    nickName = models.CharField(max_length=30, unique=False)
    bio = models.TextField(blank=True)
    profilePhoto = models.ImageField(upload_to=None, height_field=None, width_field=None, max_length=None, blank=True)
    coverPhoto = models.ImageField(upload_to=None, height_field=None, width_field=None, max_length=None, blank=True)
    price = models.IntegerField()
    walletAddress = models.CharField(
        verbose_name="Wallet Address",
        max_length=42,
        unique=True,
        validators=[RegexValidator(regex=r'^0x[a-fA-F0-9]{40}$')],
        blank=True
    )
    subscribers = models.ManyToManyField(
        'auth.User',
        related_name='subscribedTo',
        blank=True,
    )

    class Meta:
        verbose_name = ("Creator")
        verbose_name_plural = ("Creators")

    def __str__(self):
        return self.nickName


# Need to remove the blank=True later, when we have other things implemented 
class Account(models.Model):

    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    nickName = models.CharField(max_length=30, unique=False)
    bio = models.TextField(blank=True)
    profilePhoto = models.ImageField(upload_to=None, height_field=None, width_field=None, max_length=None, blank=True)
    coverPhoto = models.ImageField(upload_to=None, height_field=None, width_field=None, max_length=None, blank=True)
    walletAddress = models.CharField(
        verbose_name="Wallet Address",
        max_length=42,
        unique=True,
        validators=[RegexValidator(regex=r'^0x[a-fA-F0-9]{40}$')],
        blank=True
    )
    subscribed = models.ForeignKey(Creator, on_delete=models.CASCADE, related_name='creators', blank=False)

    class Meta:
        verbose_name = ("Account")
        verbose_name_plural = ("Accounts")

    def __str__(self):
        return self.user.id

    def get_absolute_url(self):
        return reverse("Account_detail", kwargs={"pk": self.pk})


class CreatorPost(models.Model):

    uploader = models.ForeignKey(Creator, on_delete=models.CASCADE, related_name='posts')
    upload_date = models.DateTimeField(auto_now_add=True, blank=False)
    content = models.FileField(upload_to='posts_content/%Y/%m/%d/')
    caption = models.TextField(max_length=200, blank=True)

    class Meta:
        verbose_name = ("CreatorPost")
        verbose_name_plural = ("CreatorPosts")

    def __str__(self):
        return self.uploader
    
    def is_video(self):
        return self.content_type == self.ContentType.VIDEO

    def is_picture(self):
        return self.content_type == self.ContentType.PICTURE
