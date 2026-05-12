from django.shortcuts import render, get_object_or_404, redirect
from .models import Post

def index(request):
    posts = Post.objects.all().order_by('-timestamp')
    return render(request, 'board/index.html', {'posts': posts})

def create(request):
    if request.method == 'POST':
        title = request.POST['title']
        content = request.POST['content']
        category = request.POST['category']
        Post.objects.create(title=title, content=content, category=category)
        return redirect('index')
    return render(request, 'board/create.html')

def edit(request, id):
    post = get_object_or_404(Post, id=id)
    if request.method == 'POST':
        post.title = request.POST['title']
        post.content = request.POST['content']
        post.category = request.POST['category']
        post.save()
        return redirect('index')
    return render(request, 'board/edit.html', {'post': post})

def delete(request, id):
    post = get_object_or_404(Post, id=id)
    post.delete()
    return redirect('index')
