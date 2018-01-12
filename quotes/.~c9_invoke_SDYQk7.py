
from django.db import models

from django.conf import settings

# Create your models here.
User = settings.AUTH_USER_MODEL



from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.urls import reverse
from django.db import models
from django.db.models.signals import pre_save
from django.utils import timezone
from django.utils.safestring import mark_safe
from django.utils.text import slugify

from .utils import get_read_time, unique_slug_generator

class PostManager(models.Manager):
    def active(self, *args, **kwargs):
        qs = self.get_queryset().filter(
                            draft=False,
                            publish__lte=timezone.now()
                            )
        return qs


def upload_location(instance, filename):
    PostModel = instance.__class__
    new_id = PostModel.objects.order_by("id").last().id + 1
    return "%s/%s" %(new_id, filename)

class Post(models.Model):
    user            = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    content         = models.TextField()
    active           = models.BooleanField(default=True)
    updated         = models.DateTimeField(auto_now=True, auto_now_add=False)
    timestamp       = models.DateTimeField(auto_now=False, auto_now_add=True)

    objects         = PostManager()


    def __str__(self):
        if(len(self.content)<10):
            return self.content
        else:
            return self.content[:10] +"..."

    def get_absolute_url(self):
        return reverse("quotes:detail", kwargs={"pk": self.pk})

    # def get_api_url(self):
    #     return reverse("posts-api:detail", kwargs={"slug": self.slug})

    def get_like_url(self):
        return reverse("quotes:like-toggle", kwargs={"pk": self.pk})

    def get_api_likeunlike_url(self):
        return reverse("quotes:like-api-toggle", kwargs={"pk": self.pk})
    
    class Meta:
        ordering = ["-timestamp", "-updated"]

    @property
    def get_content_type(self):
        instance = self
        content_type = ContentType.objects.get_for_model(instance.__class__)
        return content_type



def pre_save_post_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
    #     instance.slug = unique_slug_generator(instance)

    # if instance.content:
    #     read_time_var = get_read_time(instance.content)
    #     instance.read_time = read_time_var


pre_save.connect(pre_save_post_receiver, sender=Post)



# class Post(models.Model):
#     author = models.ForeignKey(User,on_delete=models.CASCADE)
#     title = models.CharField(max_length=200)
#     text = models.TextField()
#     active = models.BooleanField(default=True)
#     models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name='post_likes')
#     timestamp = models.DateTimeField(auto_now_add=True)
#     updated = models.DateTimeField(auto_now=True)
    
#     class Meta:
#         ordering = ["-timestamp", "-updated"]
    