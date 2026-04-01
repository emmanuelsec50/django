from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from .forms import UpdateMemberForm, MessageForm
from .models import Members, Messages
from django.contrib.auth.models import User

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
    reciever = User.objects.get(username=username)

    messages = Messages.objects.filter(
        sender__in = [request.user, reciever],
        reciever__in = [request.user, reciever]
    ).order_by('timestamp')

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

