from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.auth import get_user
# from django.contrib.auth.models import User


from datetime import timezone
from django.urls import reverse

from Authontication.models import User
# from .views import PostAPIView

# User = get_user_model()


class Post(models.Model):
    # author = models.ForeignKey(User, on_delete=models.CASCADE)
    
    image = models.ImageField(upload_to="images/",blank=True, null=True)
    video=models.FileField(upload_to='post_video', null=True, blank=True)
    title = models.TextField(max_length=30, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    content=models.TextField()
    auth = models.CharField(max_length=50)

    def __str__(self):
        return self.title
    # def get_author(self,obj):
    #     return obj.author.username
    # @property
    # def author(self):
        # return self.get_author()==self.author

    # def get_absolute_url(self):
    #     return reverse('post-detail', kwargs={'slug':self.slug})

class Comment(models.Model):
    pass
#     post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
#     author = models.ForeignKey(User,on_delete=models.CASCADE)
#     inst = models.ForeignKey(partnershipsInsitutions, on_delete=models.CASCADE)

#     content = models.TextField(max_length=255)
#     created_at = models.DateTimeField(auto_now_add=True)
#     parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE)
#     is_active = models.BooleanField(default=True)

#     class Meta:
#         ordering = ('-created_at',)

#     def __str__(self):
#         return f'Comment by {self.author.username} on {self.post}'

#     def children(self):
#         return Comment.objects.filter(parent=self)

#     @property
#     def is_parent(self):
#         if self.parent is not None:
#             return False
#         return True