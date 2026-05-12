from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from .models import Post

def index(request):
    posts = Post.objects.all().order_by('-timestamp')
    return render(request, 'board/index.html', {'posts': posts})

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('index')
    else:
        form = UserCreationForm()
    return render(request, 'board/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('index')
    else:
        form = AuthenticationForm()
    return render(request, 'board/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('index')

@login_required
def create(request):
    if request.method == 'POST':
        title = request.POST['title']
        content = request.POST['content']
        category = request.POST['category']
        Post.objects.create(title=title, content=content, 
                          category=category, author=request.user)
        return redirect('index')
    return render(request, 'board/create.html')

@login_required
def edit(request, id):
    post = get_object_or_404(Post, id=id, author=request.user)
    if request.method == 'POST':
        post.title = request.POST['title']
        post.content = request.POST['content']
        post.category = request.POST['category']
        post.save()
        return redirect('index')
    return render(request, 'board/edit.html', {'post': post})

@login_required
def delete(request, id):
    post = get_object_or_404(Post, id=id, author=request.user)
    post.delete()
    return redirect('index')