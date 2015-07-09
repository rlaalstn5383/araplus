from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from apps.session.models import UserProfile, Message, Block
from django.contrib.auth.decorators import login_required


def user_login(request):
    if request.method != 'POST':
        return render(request, 'session/login.html',
                      {'next': request.GET.get('next', '/')})
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username, password=password)

    if user is not None and user.is_active:
        login(request, user)
        return redirect(request.POST['next'])
    else:
        error = "Invalid login"
    return render(request, 'session/login.html', {'error': error})


def user_logout(request):
    if request.user.is_authenticated():
        logout(request)
    return redirect('/session/login')


def user_register(request):
    if request.method != "POST":
        return render(request, 'session/register.html')
    username = request.POST['username']
    password = request.POST['password']
    if password != request.POST['password_confirmation']:
        error = "Password doesn't match the confirmation"
        return render(request, "session/register.html", {'error': error})
    email = request.POST['email']
    first_name = request.POST['first_name']
    last_name = request.POST['last_name']
    new_user = User.objects.create_user(username=username,
                                        email=email,
                                        password=password,
                                        first_name=first_name,
                                        last_name=last_name)
    nickname = request.POST['nickname']
    UserProfile.objects.create(user=new_user, nickname=nickname)
    return render(request, 'session/register_complete.html')


@login_required(login_url='/session/login/')
def send_message(request):
    if request.method != "POST":
        return render(request, 'session/write_message.html')
    sender = request.user.userprofile
    content = request.POST['content']
    receiver = UserProfile.objects.get(nickname=request.POST['nickname'])
    Message.objects.create(content=content,
                           sender=sender,
                           receiver=receiver,
                           is_read=False)
    return render(request, 'session/message_success.html')


@login_required(login_url='/session/login/')
def check_message(request):
    receiver = request.user.userprofile
    blocks = Block.objects.filter(receiver=receiver)
    messages = Message.objects.filter(receiver=receiver)
    for block in blocks:
        messages = messages.exclude(sender=block.sender)
    for message in messages:
        message.read()
    return render(request,
                  'session/check_message.html', {'messages': messages})


@login_required(login_url='/session/login/')
def check_sent_message(request):
    messages = Message.objects.filter(sender=request.user.userprofile)
    return render(request,
                  'session/check_message.html', {'messages': messages})


@login_required(login_url='/session/login')
def block(request):
    if request.method != "POST":
        return render(request, 'session/block.html')
    receiver = request.user.userprofile
    sender = UserProfile.objects.get(nickname=request.POST['nickname'])
    Block.objects.create(sender=sender, receiver=receiver)
    return render(request, 'session/block_success.html')
