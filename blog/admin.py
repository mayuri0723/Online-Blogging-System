from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from import_export import resources
from .models import Post,Comment,Contact,UserProfile
#from django.contrib.auth.models import User

# Register your models here.
@admin.register(Post)

#admin.site.register(Comment)
class BlogAdmin(ImportExportModelAdmin):
   pass
class PostModelAdmin(admin.ModelAdmin):
 list_display = ['id','title','desc','date_added']
 
@admin.register(Comment)
class CommentAdmin(ImportExportModelAdmin):
   pass
class CommentModelAdmin(admin.ModelAdmin):
   list_display = ['post','author','text','created_date'] 

@admin.register(Contact)
class ContactAdmin(ImportExportModelAdmin):
  pass
class ContactModelAdmin(admin.ModelAdmin):  
  list_display = ['firstname','lastname','email','phone_no','message','date']

#user
@admin.register(UserProfile)
class UserProfileAdmin(ImportExportModelAdmin):
   pass
class UserProfileModelAdmin(admin.ModelAdmin):
   list_display=['username','firstname','lastname','email']
