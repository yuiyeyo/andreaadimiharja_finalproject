from django.db import models
from django.contrib.auth.models import User  
from django.utils import timezone

#class Profile(models.Model):
#    user = models.OneToOneField(User, on_delete=models.CASCADE)
#    interests = models.TextField(blank=True)  
#    subscriptions = models.TextField(blank=True)  
#    favorite_editors = models.ManyToManyField(User, related_name='favorited_by', blank=True)
#    disliked_topics = models.TextField(blank=True)  
#
#    def __str__(self):
#        return self.user.username

#class Notification(models.Model):
#    user = models.ForeignKey(User, on_delete=models.CASCADE)
#    message = models.TextField()
#    created_at = models.DateTimeField(default=timezone.now)
#    read = models.BooleanField(default=False)
#
#    def __str__(self):
#        return f"Notification for {self.user.username}: {self.message[:20]}"


class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name



class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  
    message = models.TextField()
    read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"To {self.user.username}: {self.message}"



#class Notification(models.Model):
#    user = models.ForeignKey(User, on_delete=models.CASCADE)


#class Notification(models.Model):
#    user = models.ForeignKey(User, on_delete=models.CASCADE)
#    message = models.TextField()
#    read = models.BooleanField(default=False)
#    timestamp = models.DateTimeField(auto_now_add=True)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    interests = models.JSONField(default=list, blank=True)
    subscriptions = models.JSONField(default=list, blank=True)
    disliked_topics = models.JSONField(default=list, blank=True)  
    notify_setting = models.CharField(max_length=20, default="daily")  
    favorite_creators = models.ManyToManyField(User, symmetrical=False, blank=True, related_name='favorited_by')

    def __str__(self):
        return self.user.username


class Advertisement(models.Model):
    headline = models.CharField(max_length=255)
    file_url = models.URLField()
    file_type = models.CharField(max_length=10, choices=[('image', 'Image'), ('video', 'Video')])
    css_class = models.CharField(max_length=100, blank=True, null=True)
    article = models.ForeignKey('Article', on_delete=models.CASCADE, related_name='ads')  # link to Article
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.headline} (Ad for: {self.article.headline})"



class Article(models.Model):
    article_id = models.AutoField(primary_key=True)
    headline = models.CharField(max_length=255)
    content = models.TextField()
    image_url = models.URLField(blank=True, null=True) 
    video_url = models.URLField(blank=True, null=True)  
    image_filename = models.CharField(max_length=255, blank=True, null=True)
    video_filename = models.CharField(max_length=255, blank=True, null=True)
    likes = models.IntegerField(default=0)
    tags = models.ManyToManyField(Tag, blank=True)
    pokemon = models.CharField(max_length=50, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    creator = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='articles',
        default=1
    )

    def get_image_url(self):
        if self.image_url:
            return self.image_url
        if self.image_filename:
            return f"https://raw.githubusercontent.com/yuiyeyo/andreaadimiharja_hw4/refs/heads/main/assets/{self.image_filename}"
        return ""

    def __str__(self):
        return self.headline

class Creator(models.Model):
    name = models.CharField(max_length=100)
    user = models.OneToOneField(User, on_delete=models.CASCADE)


#class Article(models.Model):
#    article_id = models.AutoField(primary_key=True)
#    headline = models.CharField(max_length=255)
#    content = models.TextField()
#    image_url = models.URLField(blank=True, null=True) 
#    video_url = models.URLField(blank=True, null=True)  
#    image_filename = models.CharField(max_length=255, blank=True, null=True)
#    video_filename = models.CharField(max_length=255, blank=True, null=True)
#    likes = models.IntegerField(default=0)
#    pokemon = models.CharField(max_length=50, blank=True, null=True)
#    city = models.CharField(max_length=100, blank=True, null=True)
#
#    def get_image_url(self):
#        if self.image_url:
#            return self.image_url
#        if self.image_filename:
#            return f"https://raw.githubusercontent.com/yuiyeyo/andreaadimiharja_hw4/refs/heads/main/assets/{self.image_filename}"
#        return ""
#
#
#    def __str__(self):
#        return self.headline

    
class Comment(models.Model):
    article = models.ForeignKey('Article', on_delete=models.CASCADE, related_name='comments')
    name = models.CharField(max_length=255, default="Jane Doe") 
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)  

    def __str__(self):
        return f"{self.name}: {self.text[:30]}" 
    

class VisualContent(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    file_url = models.URLField(blank=True, null=True) 
    file_type = models.CharField(max_length=10, choices=[("image", "Image"), ("video", "Video")])
    css_class = models.CharField(max_length=100, blank=True, null=True)
    article = models.ForeignKey(Article, on_delete=models.CASCADE, null=True, blank=True) 

    def __str__(self):
        return self.name
