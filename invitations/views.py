from .models import Event, AppUser, Rsvp
from .forms import EventForm, EventEditForm
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login, authenticate, get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required

from .forms import SignUpForm

User = get_user_model()

def welcome(request):
    return render(request, 'welcome.html')

def register(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login (request, user)
            return redirect('user_profile', user.pk)
    else:
        form = SignUpForm()
    return render(request, 'users/register.html', {'form': form})

@login_required
def user_profile(request, pk):
    events = Event.objects.filter(creator = request.user)
    invitations = request.user.invited_events.all()
    invitation_count = request.user.invited_events.all().count()
    to_rsvps = Rsvp.objects.get(invitee = request.user)
    return render(request, 'users/user_profile.html', {'events': events, 'invitations': invitations, 'invitation_count': invitation_count, 'to_rsvps': to_rsvps})

@login_required
def events(request):
    return True

@login_required
def event(request, pk):
    event = Event.objects.get(pk=pk)
    invitation_count = event.invitees.all().count()
    invitees = event.invitees.all()
    user = request.user
    creator = event.is_creator(user)
    return render(request, 'events/event.html', {'event': event, 'invitation_count': invitation_count, 'invitees': invitees, 'is_creator': creator})

@login_required
def event_new(request):
    if request.method == 'POST':
        form = EventForm(request.POST)
        invitees_keys = form['invitees'].value()
        user = request.user
        if form.is_valid():
            new_event = form.save(commit=False)
            new_event.creator = request.user
            new_event.save()
            new_event.invite_people(invitees_keys)
            return redirect('user_profile', user.pk)
    else:
        form = EventForm()
    return render(request, 'events/event_edit.html', {'form': form})

@login_required
def event_edit(request, pk):
    event = get_object_or_404(Event, pk=pk)
    if request.method == "POST":
        form = EventEditForm(request.POST, instance=event)
        if form.is_valid():
            event = form.save(commit=False)
            event.creator = request.user
            event.save()
            return redirect('event', pk=event.pk)
    else:
        form = EventEditForm(instance=event)
        return render(request, 'events/event_edit.html', {'form': form})

@login_required
def event_destroy(request, pk):
    event = get_object_or_404(Event, pk=pk)
    event.delete()
    return redirect('user_profile', request.user.pk)
