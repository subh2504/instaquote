
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
                            active=True
                            )
        return qs

# p = Picture.objects.get(...)
# number_of_likes = p.like_set.all().count()

class Post(models.Model):
    user            = models.ForeignKey(User,on_delete=models.CASCADE)
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
        
class Like(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    post = models.ForeignKey(Post,on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ["-created"]
        unique_together = (("user", "post"),)
        
    def __str__(self):
        return str(self.user.id)+ " "+str(self.post)


def pre_save_post_receiver(sender, instance, *args, **kwargs):
    pass
    # if not instance.slug:
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
    