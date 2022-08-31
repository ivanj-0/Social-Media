from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Post(models.Model):
   
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='post_images')
    caption = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add = True)  
    no_likes = models.IntegerField(default=0)
    no_flags = models.IntegerField(default=0)
    
    

    def __str__(self):
        return str(self.created_at) + " : " + self.user.username

class Comment(models.Model):
    comment = models.CharField(max_length=500)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, null=True, blank=True, on_delete=models.CASCADE)
    no_flags_c = models.IntegerField(default=0)
    def __str__(self):
        return self.comment

    def get_profile_img(self):
        profile = Profile.objects.get(user=self.user)
        return profile.profileimg.url

class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(blank=True)
    profileimg = models.ImageField(upload_to='profile_images', default='/media/blank-profile-picture.png')
    location = models.CharField(max_length=100, blank=True)
    pref = models.BooleanField(default = True)
    following = models.ManyToManyField(User,related_name="followed_by",symmetrical=False,blank=True)
    followers = models.ManyToManyField(User,related_name="following",symmetrical=False,blank=True)
    likes = models.ManyToManyField(Post,related_name="liked_post",symmetrical=False,blank=True)
    def __str__(self):
        return self.user.username
    flagsp = models.ManyToManyField(Post,related_name="flagged_post",symmetrical=False,blank=True)
    flagsc = models.ManyToManyField(Comment,related_name="flagged_comment",symmetrical=False,blank=True)



