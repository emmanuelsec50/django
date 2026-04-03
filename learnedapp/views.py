from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from .forms import UpdateMemberForm, MessageForm
from .models import Members, Messages
from django.contrib.auth.models import User
from django.db.models import Q

# Create your views here.
def register(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid:
            user = form.save()
            login(request, user)
            
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'learnedapp/register.html', {'form': form})

@login_required
def home(request):
    return render(request, 'learnedapp/home.html')

@login_required
def updatemember(request):
    member = Members.objects.get(user=request.user)
    if request.method == 'POST':
        form = UpdateMemberForm(request.POST, instance=member)
        if form.is_valid:
            form.save()
            return redirect('profile')
    else:
        form = UpdateMemberForm(instance=member)
    return render(request, 'learnedapp/edit_profile.html', {'form': form})

@login_required
def profile(request):
    member, created = Members.objects.get_or_create(user=request.user)
    context = {'member': member}
    return render(request, 'learnedapp/profile.html', context)

@login_required
def chat(request, username):
    if request.user.username == username:
        return redirect('profile')
    reciever = get_object_or_404(User, username=username) #User.objects.get(username=username)
    

    messages = Messages.objects.filter(
        sender__in = [request.user, reciever],
        reciever__in = [request.user, reciever]
    ).order_by('timestamp')

    Messages.objects.filter(
        sender = reciever,
        reciever = request.user,
        is_read = False
    ).update(is_read=True)

    if request.method == 'POST':

        form = MessageForm(request.POST)
        if form.is_valid():
            msg = form.save(commit=False)
            msg.sender = request.user
            msg.reciever = reciever
            msg.save()
            return redirect('chat', username=reciever.username)
    else:
        form = MessageForm()
    context = {'messages': messages, 'form': form, 'reciever': reciever}
    return render(request, 'learnedapp/chat.html', context)

@login_required
def chat_list(request):
    user = request.user

    messages = Messages.objects.filter(Q(sender=user) | Q(reciever=user)).order_by('-timestamp')
    conversations = {}
    for message in messages:
        if message.sender == request.user:
            other_user = message.reciever
        else:
            other_user = message.sender

        unread_messages = Messages.objects.filter(
            sender = other_user,
            reciever = user,
            is_read = False
        ).count()



        if other_user not in conversations:
            conversations[other_user] = {
                'message': message,
                'unread_messages': unread_messages
            }

    return render(request, 'learnedapp/chat_listing.html', {'conversations': conversations.items()})

@login_required
def search_user(request):
    query = request.GET.get('q')
    users = []
    if query:
        users = User.objects.filter(Q(username__icontains = query)).exclude(username = request.user.username)

    context = {
        'query': query,
        'users': users
    }
    return render(request, 'learnedapp/search_user.html', context)
