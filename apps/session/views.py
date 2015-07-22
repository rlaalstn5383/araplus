from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from apps.session.models import UserProfile, Message, Block, Group
from django.contrib.auth.decorators import login_required
from django.db.models import Q


def user_login(request):
    if request.method != 'POST':
        if request.user.is_authenticated():
            return render(request, 'session/login.html',
                          {'next': request.GET.get('next', '/session/login'),
                           'alreadyloggedin': True})
        return render(request, 'session/login.html',
                      {'next': request.GET.get('next', '/session/login')})
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
    try:
        receiver = UserProfile.objects.get(nickname=request.POST['nickname'])
    except UserProfile.DoesNotExist:
        return render(request, 'session/write_message.html',
                      {'error': "The user doesn't exist"})
    Message.objects.create(content=content,
                           sender=sender,
                           receiver=receiver,
                           is_read=False)
    success = "Successfully sent message"
    return render(request, 'session/write_message.html', {'success': success})


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
def check_thread(request, nickname):
    receiver = request.user.userprofile
    sender = UserProfile.objects.get(nickname=nickname)
    messages = Message.objects.filter(Q(sender=sender, receiver=receiver) |
                                      Q(receiver=sender, sender=receiver))
    messages = messages.order_by('created_time')
    for message in messages:
        message.read()
    return render(request,
                  'session/message_thread.html', {'sender': sender,
                                                  'receiver': receiver,
                                                  'messages': messages})


@login_required(login_url='/session/login/')
def check_sent_message(request):
    messages = Message.objects.filter(sender=request.user.userprofile)
    return render(request,
                  'session/check_sent_message.html', {'messages': messages})


@login_required(login_url='/session/login')
def block(request):
    if request.method != "POST":
        return render(request, 'session/block.html')
    receiver = request.user.userprofile
    try:
        sender = UserProfile.objects.get(nickname=request.POST['nickname'])
    except UserProfile.DoesNotExist:
        return render(request, 'session/block.html',
                      {'error': "The user doesn't exist"})
    if sender == receiver:
        return render(request, 'session/block.html',
                      {'error': "You can't block yourself"})
    if len(Block.objects.filter(sender=sender, receiver=receiver)) != 0:
        return render(request, 'session/block.html',
                      {'error': "You already blocked the user"})
    Block.objects.create(sender=sender, receiver=receiver)
    success = "block successful"
    return render(request, 'session/block.html', {'success': success})


@login_required(login_url='/session/login')
def show_block_list(request):
    if request.method != "POST":
        blocks = Block.objects.filter(receiver=request.user.userprofile)
        return render(request, 'session/block_list.html', {'blocks': blocks})

    # The rest is unblock
    try:
        blocked_UP = UserProfile.objects.get(nickname=request.POST['nickname'])
    except UserProfile.DoesNotExist:
        return render(request, 'session/block_list.html',
                      {'error': "There are no user with the given nickname"})
    block = Block.objects.get(sender=blocked_UP,
                              receiver=request.user.userprofile)
    block.delete()
    return redirect('/session/messageblocklist')


@login_required(login_url='/session/login')
def show_group_list(request):
    if request.method != "POST":
        groups = Group.objects.filter(members=request.user.userprofile)
        return render(request, 'session/group_list.html', {'groups':groups})

    return redirect('/session/group/'+request.POST['checkname'])


@login_required(login_url='/session/login')
def make_group(request):
    if request.method != "POST":
        return render(request, 'session/make_group.html')

    name = request.POST['name']
    try:
        tempgroup = Group.objects.get(name=name)
    except Group.DoesNotExist:
        newgroup=Group.objects.create(name=name)
        newgroup.add_member(request.user.userprofile)
        return redirect('/session/group/'+name+'/manage')
    return render(request, 'session/make_group.html',
                  {'error':'The name is already being used by other group'})
