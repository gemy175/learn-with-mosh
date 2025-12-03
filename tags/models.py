from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey


class TaggedItemManager(models.Manager):
    def get_tags_for(self, obj_type, obj_id):
        content_type = ContentType.objects.get_for_model(obj_type)
        
        return TaggedItem.objects \
            .select_related('tag') \
            .filter(
                content_type=content_type,
                object_id=obj_id
            )
        # then use it in taggedItem model 

class Tag(models.Model):
    label = models.CharField(max_length=255)

    def __str__(self):
        return self.label


class TaggedItem(models.Model):
    tag = models.ForeignKey(Tag , on_delete=models.CASCADE)
    # product = models.ForeignKey(Product , on_delete=models.CASCADE)
    # to make it general and can use it with any obj so :>
    # we need the type and id 
    # TYPE
    content_type = models.ForeignKey(ContentType , on_delete=models.CASCADE)
    # ID 
    object_id = models.PositiveIntegerField()

    # actual object that tag applied to 
    content_object = GenericForeignKey()

    # use custom manager here 
    objects = TaggedItemManager()


