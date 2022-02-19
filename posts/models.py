from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.db.models.signals import post_save


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    last_request = models.DateTimeField(blank=True, null=True)


def create_profile(sender, **kwargs):
    if kwargs['created']:
        profile=Profile(user=kwargs['instance'])
        profile.save()

post_save.connect(create_profile, sender=User)


class Post(models.Model):
    '''Model representing a post'''
    creator = models.ForeignKey(
        User,
        default=1,
        null=True,
        on_delete=models.SET_NULL
    )
    content = models.TextField(max_length=10000, help_text='Write new post')
    created = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(
        User,
        through='LikeDate',
        blank=True,
        related_name='likes'
    )
    dislikes = models.ManyToManyField(User, blank=True,related_name='dislikes')
    
    class Meta:
        # Sort from newest to oldest
        ordering = ['-created']
   
    def get_absolute_url(self):
        '''Return the url to access a particular post'''
        return reverse('post', args=[str(self.id)])
    
    def __str__(self):
        return f'{self.creator} - {self.created}'


class LikeDate(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    created = models.DateField(auto_now_add=True)
