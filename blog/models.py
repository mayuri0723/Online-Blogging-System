from django.db import models
models.BooleanField
models.ForeignKey
from django.utils import timezone


# Create your models here.
class Post(models.Model):
 title = models.CharField(max_length=170)
 desc = models.TextField()

 date_added= models.DateTimeField(auto_now_add = True)

#class of comment
class Comment(models.Model):
    post = models.ForeignKey('blog.Post', on_delete=models.CASCADE, related_name='comments')
    author = models.CharField(max_length=200)
    text = models.TextField()
    
    created_date = models.DateTimeField(default=timezone.now)
    approved_comment = models.BooleanField(default=False)

    def approve(self):
      self.approved_comment = True
      self.save()
      
    
    def __str__(self):
        return 'Comment {} by {}'.format(self.text, self.author)
    
    def approved_comments(self):
     return self.comments.filter(approved_comment=True)


class Contact(models.Model):
     firstname = models.CharField(max_length=120)
     lastname = models.CharField(max_length=120)
     email = models.EmailField()
     phone_no = models.CharField(max_length=12)
     date = models.DateTimeField(auto_now_add = True)
     message = models.TextField(max_length=130)
   
     def __str__(self):
      return self.firstname+"-"+self.lastname+"-"+self.email+"-"+self.phone_no+"-"+self.message

class UserProfile(models.Model):
   username  = models.CharField(max_length=120)
   email = models.EmailField()
   firstname = models.CharField(max_length=120)
   lastname = models.CharField(max_length=120)
   
   def __str__(self):
     return self.username