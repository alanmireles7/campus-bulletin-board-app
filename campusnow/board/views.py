from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from .models import Post, Comment, Reaction
from django.http import HttpResponseRedirect
from django.urls import reverse

def index(request):
    category = request.GET.get('category', '')
    posts = Post.objects.all().order_by('-timestamp')
    if category:
        posts = posts.filter(category=category)
    emojis = Reaction.EMOJI_CHOICES

    for post in posts:
        post.reaction_info = []
        for emoji, label in emojis:
            count = post.reactions.filter(emoji=emoji).count()
            reacted = False
            if request.user.is_authenticated:
                reacted = post.reactions.filter(emoji=emoji, author=request.user).exists()
            post.reaction_info.append({
                'emoji': emoji,
                'count': count,
                'reacted': reacted,
            })

    categories = [c[0] for c in Post.CATEGORY_CHOICES]
    return render(request, 'board/index.html', {
        'posts': posts,
        'emojis': emojis,
        'categories': categories,
        'selected_category': category,
    })

    return render(request, 'board/index.html', {'posts': posts, 'emojis': emojis})

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
        return HttpResponseRedirect(reverse('index') + f'#post-{id}')
    return render(request, 'board/edit.html', {'post': post})

@login_required
def delete(request, id):
    post = get_object_or_404(Post, id=id, author=request.user)
    post.delete()
    return redirect('index')

@login_required
def add_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method == 'POST':
        content = request.POST['content']
        if content.strip():
            Comment.objects.create(post=post, author=request.user, content=content)
    return HttpResponseRedirect(reverse('index') + f'#post-{post_id}')

@login_required
def delete_comment(request, id):
    comment = get_object_or_404(Comment, id=id, author=request.user)
    post_id = comment.post.id
    comment.delete()
    return HttpResponseRedirect(reverse('index') + f'#post-{post_id}')

@login_required
def react(request, post_id, emoji):
    from django.http import JsonResponse
    post = get_object_or_404(Post, id=post_id)
    existing = Reaction.objects.filter(post=post, author=request.user, emoji=emoji)
    if existing.exists():
        existing.delete()
        reacted = False
    else:
        Reaction.objects.create(post=post, author=request.user, emoji=emoji)
        reacted = True
    count = post.reactions.filter(emoji=emoji).count()
    return JsonResponse({'reacted': reacted, 'count': count})