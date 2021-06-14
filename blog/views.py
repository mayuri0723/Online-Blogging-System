
from django.shortcuts import render,redirect,get_object_or_404
from  django.http import HttpResponseRedirect
from .forms import SignUpForm, LoginForm, PostForm,CommentForm,ContactForm
from django.contrib import messages
from django.contrib.auth import authenticate, login,logout
from .models import Post,Comment,Contact,UserProfile
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required


# Create your views here.
#Home View
def home(request):
    posts = Post.objects.all()
    ordering =['-date_posted']
    return render(request,'blog/home.html',{'posts':posts})

#About View
def about(request):
    return render(request,'blog/about.html')

#Contact View
def contact(request):
     if request.method=='POST':
       form = ContactForm(request.POST)

       if form.is_valid():
        firstname = form.cleaned_data['firstname']
        lastname = form.cleaned_data['lastname']
        email = form.cleaned_data['email']
        phone_no = form.cleaned_data['phone_no']
        message=form.cleaned_data['message']
        contact = Contact(firstname=firstname, lastname=lastname, email=email, phone_no=phone_no, message=message)
        contact= form.save()
        messages.success(request,"Thanks for contacting us!.")
       # return HttpResponseRedirect('blog/contact.html',{'form':form})
        
     else:
        form=ContactForm()
        contacts = Contact.objects.all()
     return render(request,'blog/contact.html',{'form':form, 'contacts':contacts})
   

#Dashboard View
def dashboard(request):
    if  request.user.is_authenticated:
        posts = Post.objects.all()
        user =  request.user
        #method for using full name
        full_name = user.get_full_name()
        #here gps means groups
        gps = user.groups.all()
        return render(request,'blog/dashboard.html',{'posts':posts,
        'full_name':full_name,'groups':gps})
    else:
       return  HttpResponseRedirect('/login/') 

#Signup View
def user_signup(request):
    if request.method == "POST":

      form = SignUpForm(request.POST)
      if form.is_valid():
        username = form.cleaned_data['username']
        firstname = form.cleaned_data['first_name']
        lastname = form.cleaned_data['last_name']
        email = form.cleaned_data['email']
        print(username)
        user = UserProfile(username=username,firstname=firstname,lastname=lastname,email=email)
        user= user.save()
        messages.success(request,'Congratulations!! You have become an Author.')
        user = form.save()
        group = Group.objects.get(name='Author')
        user.groups.add(group)
    else:
     form = SignUpForm()
    return render(request,'blog/signup.html',{'form':form})

#Login View
def user_login(request):
 if not request.user.is_authenticated:
    flag=False
    if request.method =="POST":
        
        form = LoginForm(request=request, data =request.POST)
        if form.is_valid():
            uname = form.cleaned_data['username']
            upass = form.cleaned_data['password']
            user = authenticate(username=uname,password=upass)
            if user is not None:
                login(request, user)
                messages.success(request,"Logged in successfully")
                flag=True
        if(not flag):
           messages.success(request,"Invalid user")
        return HttpResponseRedirect('/dashboard/')
    else:
     form = LoginForm()
     return render(request,'blog/login.html',{'form':form})
 else:
     return HttpResponseRedirect('/dashboard/')   
# def user_login(request):
#  if not request.user.is_authenticated:
#     if request.method =="POST":
#         form = LoginForm(request=request, data =request.POST)
#         if form.is_valid():
#             uname = form.cleaned_data['username']
#             upass = form.cleaned_data['password']
#             user = authenticate(username=uname,password=upass)
#             if user is not None:
#              login(request,user)

#              if  uname=='admin' and  upass=='admin':
#                   messages.success(request,' Admin Logged in Successfully!')
#              else:
#                   messages.success(request,'Logged in Successfully!')
#             return HttpResponseRedirect('/dashboard/')
#     else:
#      form = LoginForm()
#      return render(request,'blog/login.html',{'form':form})
#  else:
#      return HttpResponseRedirect('/dashboard/')   


#Logout View
def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/')

#Add new Post
def add_post(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
         form = PostForm(request.POST)
         if form.is_valid():
            title = form.cleaned_data['title']
            desc = form.cleaned_data['desc']
            pst = Post(title=title, desc=desc)
            pst.save()
            messages.success(request,'Post added Successfully!')
            form = PostForm()
        else:
            form = PostForm()   
        return render(request,'blog/addpost.html',{'form':form})
    else:
        return HttpResponseRedirect('/dashboard/')
         

#Update Post
def update_post(request,id):
    if request.user.is_authenticated:
        if request.method == 'POST':
          pi = Post.objects.get(pk=id)  
          form = PostForm(request.POST, instance=pi) 
          if form.is_valid():
            form.save()
            messages.success(request,'Updated Post Successfully!')
        else:
            pi = Post.objects.get(pk=id) 
            form = PostForm(instance=pi)     
        return render(request,'blog/updatepost.html',{'form':form})
    else:
       return HttpResponseRedirect('/dashboard/')

#delete Post
def delete_post(request,id):
    if request.user.is_authenticated:
        if request.method == 'POST':
            pi = Post.objects.get(pk=id) 
            pi.delete()
            messages.success(request,'deleted Post Successfully!')
            return HttpResponseRedirect('/dashboard/')
    else:
        return HttpResponseRedirect('/login/')

#to Add Comment
def add_comment_to_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author=request.user.username
            comment.save()
            messages.success(request,'Commented in Successfully!')
            return redirect('/dashboard/', pk=post.pk)
    else:
        form = CommentForm()
    return render(request, 'blog/add_comment_to_post.html', {'form': form})


#Login Required
@login_required
def comment_approve(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.approve()
    return redirect('post_detail', pk=comment.post.pk)

@login_required
def comment_remove(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.delete()
    messages.success(request,'Comment deleted in Successfully!')
    return redirect('/dashboard/', pk=comment.post.pk)

#Search Code
def search(request):
    query=request.POST['query']
    posts= Post.objects.filter(title=query)
    params={'posts': posts}
    #msg no result found
    #messages.success(request,'No Search Result Found!')
    return render(request, 'blog/search.html', params)

