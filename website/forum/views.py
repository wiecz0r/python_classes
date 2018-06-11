from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .models import Post, Thread, Topic
from django.utils import timezone
from .forms import TopicForm, LoginForm, PostForm, RegisterForm
from django.contrib.auth import authenticate, login, logout


# Create your views here.

def topics(request):
    sorted_topics = Topic.objects.order_by('timestamp')
    context = {'sorted_topics': sorted_topics}
    return render(request, 'forum/topics.html', context)


@login_required
def add_topic(request):
    if request.method == 'POST':
        form = TopicForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            new_topic = Topic(name=data.get('name'), timestamp=timezone.now(), user_id=request.user)
            new_topic.save()
            return HttpResponseRedirect('/')
    else:
        form = TopicForm()
    return render(request, 'forum/add_topic.html', {'form': form})


def threads(request, topic_id):
    sorted_threads = Thread.objects.filter(topic_id=topic_id)
    topic_name = Topic.objects.get(id=topic_id).name
    context = {'threads': sorted_threads, 'topic_id': topic_id, 'topic_name': topic_name}
    return render(request, 'forum/threads.html', context)


@login_required
def add_thread(request, topic_id):
    if request.method == 'POST':
        form = TopicForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            new_thread = Thread(
                title=data.get('name'),
                timestamp=timezone.now(),
                topic_id=Topic.objects.get(id=topic_id),
                user_id=User.objects.get(username=request.user)
            )
            new_thread.save()
            url = '/' + str(topic_id) + '/'
            return HttpResponseRedirect(url)
    else:
        form = TopicForm()
    return render(request, 'forum/add_topic.html', {'form': form, 'name': (str(topic_id) + '/add_thread')})


def posts(request, thread_id):
    thread = Thread.objects.get(id=thread_id)
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            new_post = Post(
                text=data.get('text'),
                user_id=User.objects.get(username=request.user),
                thread_id=thread,
                pub_date=timezone.now()
            )
            new_post.save()

            return HttpResponseRedirect('../{}'.format(thread_id))
    else:
        form = PostForm()
    posts_sorted = Post.objects.filter(thread_id=thread_id).order_by('pub_date')
    thread_name = Thread.objects.get(id=thread_id).title
    context = {'posts': posts_sorted,
               'thread': thread_name,
               'form': form,
               }
    return render(request, 'forum/posts.html', context)


@login_required
def delete(request, arg):
    args = str(arg).split('-')
    print(args)
    if args[0] == 'post':
        Post.objects.get(id=args[1]).delete()
        print('Post deleted')
    elif args[0] == 'thread':
        Thread.objects.get(id=args[1]).delete()
        print('Thread deleted')
    elif args[0] == 'topic':
        Topic.objects.get(id=args[1]).delete()
        print('Topic deleted')

    url = request.META.get('HTTP_REFERER')
    if url is None:
        url = '/'
    return HttpResponseRedirect(url)


def login_page(request):
    logged = None
    url = '/'
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = authenticate(request, username=data.get('username'), password=data.get('password'))
            if user is not None:
                login(request, user)
                if request.POST['url'] != 'None':
                    url = request.POST['url']
                logged = True
            else:
                logged = False
    else:
        url = request.META.get('HTTP_REFERER')
        form = LoginForm()
    return render(request, 'forum/auth.html', {'form': form, 'url': url, 'logged': logged})


def register(request):
    logged = None
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = User.objects.create_user(
                username=data['username'],
                password=data['password'],
                email=data['email'],
                first_name=data['first'],
                last_name=data['last']
            )
            user.save()
            login(request, user)
            logged = True
    else:
        form = RegisterForm()
    return render(request, 'forum/register.html', {'form': form, 'logged': logged})


def log_out(request):
    logout(request)
    url = request.META.get('HTTP_REFERER')
    if url is None:
        url = '/'
    return HttpResponseRedirect(url)


@login_required
def my_info(request):
    url = request.META.get('HTTP_REFERER')
    if url is None:
        url = '/'
    context = {'url': url}
    return render(request, 'forum/profile.html', context)
