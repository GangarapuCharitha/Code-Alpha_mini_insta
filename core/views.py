from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth import login, authenticate, logout
from .forms import SignUpForm, PostForm
from .models import Post, Like,Comment
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from django.contrib.admin.views.decorators import staff_member_required

def home_view(request):
    return render(request, 'home.html')
def signup_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists.')
            return redirect('signup')

        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()

        messages.success(request, 'Account created! Please log in.')
        return redirect('login')

    return render(request, 'signup.html')

def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)

        # Pull the submitted username *before* validation so we can look it up
        submitted_username = request.POST.get("username")

        if form.is_valid():                          # <— credentials are correct
            user = form.get_user()
            login(request, user)
            return redirect('profile', username=user.username)
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('index')

@login_required
def index(request):
    posts = Post.objects.all().order_by('-created')
    form = PostForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        post = form.save(commit=False)
        post.user = request.user
        post.save()
        return redirect('index')
    return render(request, 'index.html', {'posts': posts, 'form': form})

@login_required
def like_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    like, created = Like.objects.get_or_create(user=request.user, post=post)
    if not created:
        like.delete()  # Toggle like
    return redirect('feed')  
@login_required
def profile(request, username):
    from django.contrib.auth.models import User
    user = User.objects.get(username=username)
    posts = Post.objects.filter(user=user)
    return render(request, 'profile.html', {'profile_user': user, 'posts': posts})
def all_users_view(request):
    users = User.objects.all()  # get all users
    return render(request, 'all_users.html', {'users': users})
def profile_redirect_view(request):
    if request.user.is_authenticated:
        return redirect('profile', username=request.user.username)
    else:
        
        return redirect('login')
def profile_view(request, username):
    user = get_object_or_404(User, username=username)
    posts = Post.objects.filter(user=user).order_by('-created')  # posts of this user
    context = {
        'profile_user': user,
        'posts': posts,
    }
    return render(request, 'profile.html', context)

@login_required
def add_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            return redirect('profile')  # redirect back to profile after adding
    else:
        form = PostForm()
    return render(request, 'add_post.html', {'form': form})
@login_required
def profile_view(request, username):
    user = get_object_or_404(User, username=username)
    posts = Post.objects.filter(user=user).order_by('-created')
    return render(request, 'profile.html', {'profile_user': user, 'posts': posts})
@login_required
def feed_view(request):
    posts = Post.objects.all().order_by('-created')  # or 'created' field depending on your model
    return render(request, 'feed.html', {'posts': posts})
@login_required
def comment_post(request, post_id):
    if request.method == "POST":
        post = get_object_or_404(Post, id=post_id)
        content = request.POST.get('content')
        if content:
            Comment.objects.create(user=request.user, post=post, content=content)
    return redirect('feed')