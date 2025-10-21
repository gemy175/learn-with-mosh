from django.db import models
from django.contrib .contenttypes.models import ContentType
from django.contrib .contenttypes.fields import GenericForeignKey

# Create your models here.

class Tag(models.Model):
    label = models.CharField(max_length=255)


class TaagedItem(models.Model):
    tag = models.ForeignKey(Tag , on_delete=models.CASCADE)
    # product = models.ForeignKey(Product , on_delete=models.CASCADE)
    # we need the type and id 
    # TYPE
    content_type = models.ForeignKey(ContentType , on_delete=models.CASCADE)
    # ID 
    object_id = models.PositiveIntegerField()

    # actual object that tag applied to 
    content_object = GenericForeignKey()
