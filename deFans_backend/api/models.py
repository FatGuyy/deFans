import uuid
from django.db import models
from django.urls import reverse
from django.core.validators import RegexValidator

class Creator(models.Model):
    id = models.UUIDField(primary_key=True, default= uuid.uuid4)
    userName = models.CharField(max_length=15, unique=True)
    nickName = models.CharField(max_length=30, unique=False)
    bio = models.TextField(blank=True)
    profilePhoto = models.ImageField(upload_to=None, height_field=None, width_field=None, max_length=None)
    coverPhoto = models.ImageField(upload_to=None, height_field=None, width_field=None, max_length=None)
    price = models.IntegerField()
    walletAddress = models.CharField(
        verbose_name="Wallet Address",
        max_length=42,
        unique=True,
        validators=[RegexValidator(regex=r'^0x[a-fA-F0-9]{40}$')],
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
        return self.userName

    def get_absolute_url(self):
        return reverse("Creator_detail", kwargs={"pk": self.pk})


class User(models.Model):
    id = models.UUIDField(primary_key=True, default= uuid.uuid4)
    userName = models.CharField(max_length=15, unique=True)
    nickName = models.CharField(max_length=30, unique=False)
    bio = models.TextField(blank=True)
    profilePhoto = models.ImageField(upload_to=None, height_field=None, width_field=None, max_length=None, blank=True)
    coverPhoto = models.ImageField(upload_to=None, height_field=None, width_field=None, max_length=None, blank=True)
    walletAddress = models.CharField(
        verbose_name="Wallet Address",
        max_length=42,
        unique=True,
        validators=[RegexValidator(regex=r'^0x[a-fA-F0-9]{40}$')],
        blank=False
    )
    subscribed = models.ForeignKey(Creator, on_delete=models.CASCADE, related_name='creators', blank=False)

    class Meta:
        verbose_name = ("User")
        verbose_name_plural = ("Users")

    def __str__(self):
        return self.userName

    def get_absolute_url(self):
        return reverse("User_detail", kwargs={"pk": self.pk})

class CreatorPost(models.Model):
    id = models.UUIDField(primary_key=True, default= uuid.uuid4)
    uploader = models.ForeignKey(Creator, on_delete=models.CASCADE, related_name='uploaded_posts')
    upload_date = models.DateTimeField(auto_now_add=True, blank=False)
    content = models.FileField(upload_to='posts_content/%Y/%m/%d/')
    caption = models.TextField(max_length=200, blank=True)

    class Meta:
        verbose_name = ("CreatorPost")
        verbose_name_plural = ("CreatorPosts")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("CreatorPost_detail", kwargs={"pk": self.pk})
    
    def is_video(self):
        return self.content_type == self.ContentType.VIDEO

    def is_picture(self):
        return self.content_type == self.ContentType.PICTURE
