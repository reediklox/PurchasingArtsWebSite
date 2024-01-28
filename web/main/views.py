from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from .models import Users, Posts, Comments, UsersRights, Likes, Marks
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from .forms import UserRegistrationForm, LikeForm, AddPost, AddComment
from django.shortcuts import get_object_or_404
from random import randint


def getIP(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[-1].strip()
    else:
        ip = request.META.get('REMOTE_ADDR')
    
    return f'user-{ip.split('.')[0]}'

#################
#Work with posts#
#################

def general(request):
    posts = Posts.objects.all().order_by('-post_date')
    comm = Comments.objects.all().order_by('-comment_date')
    try:
        comms = [Comments.objects.all().order_by('-comment_date')[0]]
    
        for com in comm:    
            for i in comms:
                if com.post_id != i.post_id:
                    comms.append(com)
    except IndexError: comms = []
    
    return render(request, 'posts.html', {'posts': posts, 'comms': comms, 'user_ip': getIP(request), 'user': request.user})

def post(request, post_id):
    try:
        post = Posts.objects.get(post_id=post_id)
    except:
        return HttpResponse(f"<h1>Was not found (404)</h1> <h2>Post with id {post_id}</h2>")
        
    comms = Comments.objects.all().filter(post_id=post).order_by('-comment_date')
    
    return render(request, 'post.html', {'post': post, 'comms': comms, 'user_ip': getIP(request), 'user': request.user})

def popular(request):
    posts = Posts.objects.all().order_by('-post_likes')
    comm = Comments.objects.all().order_by('-comment_date')
    try:
        comms = [Comments.objects.all().order_by('-comment_date')[0]]
    
        for com in comm:    
            for i in comms:
                if com.post_id != i.post_id:
                    comms.append(com)
    except IndexError: comms = []
                
    return render(request, 'popular.html', {'posts': posts, 'comms': comms, 'user_ip': getIP(request), 'user': request.user})

def category(request, post_category):
    posts = Posts.objects.all().filter(post_category=post_category)
    comm = Comments.objects.all().order_by('-comment_date')
    try:
        comms = [Comments.objects.all().order_by('-comment_date')[0]]
    
        for com in comm:    
            for i in comms:
                if com.post_id != i.post_id:
                    comms.append(com)
    except IndexError: comms = []
    
    return render(request, 'categories.html', {'posts': posts, 'comms': comm, 'user_ip': getIP(request), 'user': request.user})

#################################
         

#################################
#Work with user login/reg/logout#
#################################

def registration(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('login')
    else:
        form = UserRegistrationForm()
    
    return render(request, 'reg.html', {'form': form, 'user_ip': getIP(request), 'user': request.user})

def user_login(request):
    if request.method == 'POST':
        login_form = AuthenticationForm(request, request.POST)
        if login_form.is_valid():
            user = login_form.get_user()
            login(request, user)
            return redirect('home')
    else:
        login_form = AuthenticationForm()
    return render(request, 'login.html', {'form': login_form, 'user_ip': getIP(request), 'user': request.user})

def user_logout(request):
    if request.method == 'GET':
        logout(request)
        return redirect('home')

################################


######################
#Work with login user#
######################

def profile(request):
    user = request.user
    posts = Posts.objects.all().filter(author_login=user)
    return render(request, 'profile.html', {'user': user, 'posts': posts})

def like_post(request, post_id):
    post = get_object_or_404(Posts, post_id=post_id)

    if request.method == 'POST':
        form = LikeForm(request.POST)
        if form.is_valid():
            existing_like = Likes.objects.filter(user=request.user, post=post)

            if existing_like.exists():
                existing_like.delete()

                post.post_likes -= 1
                post.save()

                return JsonResponse({'message': 'unliked'}, safe=False)
            else:
                like = form.save(commit=False)
                like.user = request.user
                like.post = post
                like.save()

                Marks.objects.create(likes=like)
                
                post.post_likes += 1
                post.save()

                return JsonResponse({'message': 'success'}, safe=False)

    return JsonResponse({'message': 'not_a_post_request'}, safe=False)

def marks(request):
    marks = Marks.objects.all().filter(likes__user=request.user)
    comm = Comments.objects.all().order_by('-comment_date')
    try:
        comms = [Comments.objects.all().order_by('-comment_date')[0]]
    
        for com in comm:    
            for i in comms:
                if com.post_id != i.post_id:
                    comms.append(com)
    except IndexError: comms = []
    
    return render(request, 'marks.html', {'marks': marks, 'comms': comm, 'user': request.user})

def addPost(request):
    if request.method == 'POST':
        form = AddPost(request.POST, request.FILES)
        
        if form.is_valid():
            post = Posts()
            post.author_login = request.user
            post.post_title = form.cleaned_data['post_title']
            post.post_category = form.cleaned_data['post_category']
            post.post_image = form.cleaned_data['post_image']
            post.img_price = form.cleaned_data['img_price']
            
            post.save()
            
            return redirect('post', post.post_id)
    else:
        form = AddPost()
    return render(request, 'add.html', {'form': form, 'user': request.user})

def imgChange(request):
    user = request.user
    posts = Posts.objects.all().filter(author_login=user)
    if request.method == 'POST':
        file = request.FILES['profile_image']
        
        user.profile_image = file
        user.save()
        
        return redirect('profile')
    
    return render(request, 'profile.html', {'user': user, 'posts': posts})

def addComment(request, post_id):
    try:
        post = Posts.objects.get(post_id=post_id)
    except:
        return HttpResponse(f"<h1>Was not found (404)</h1> <h2>Post with id {post_id}</h2>")
        
    comms = Comments.objects.all().filter(post_id=post).order_by('-comment_date')
    
    if request.method == 'POST':
        form = AddComment(request.POST)
        if form.is_valid():
            comment = Comments()
            
            comment.author_login = request.user
            comment.post_id = post
            comment.comment_content = form.cleaned_data['comment_content']
            comment.save()
            
            return redirect('post', post_id)
    else:
        form = AddComment()
    return render(request, 'post.html', {'form': form, 'post': post, 'comms': comms, 'user_ip': getIP(request), 'user': request.user})

def buy(request, post_id):
    try:
        post = Posts.objects.get(post_id=post_id)
    except:
        return HttpResponse(f"<h1>Was not found (404)</h1> <h2>Post with id {post_id}</h2>")
    comms = Comments.objects.all().filter(post_id=post).order_by('-comment_date')
    user = request.user
    
    if request.method == 'POST':
        value = randint(0, 1)
        if value:
            uRight = UsersRights()
            uRight.author_login = user
            uRight.post_id = post

            uRight.save()
            
            post.author_login = user
            post.save()
            
            return redirect('post', post_id)
        else:
            return HttpResponse('<h1>Не достаточно средств!<h1>')
    
    return render(request, 'post.html', {'post': post, 'comms': comms, 'user': user})

def history(request):
    rights = UsersRights.objects.all().filter(author_login=request.user)
    return render(request, 'history.html', {'user': request.user, 'rights': rights})  