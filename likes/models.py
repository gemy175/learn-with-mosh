from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType


class likedItem(models.Model):
    user = models.ForeignKey(User , on_delete=models.CASCADE)

    # type , id , generic object
    content_type = models.ForeignKey(ContentType ,on_delete=models.PROTECT)

    object_id = models.PositiveIntegerField()

    content_object = GenericForeignKey()