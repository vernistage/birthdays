from .models import (
    Event, AppUser,
    Rsvp
)
from .forms import (
    EventForm, EventForm,
    RsvpEditForm
)
from django.shortcuts import (
    render, get_object_or_404,
    redirect
)
from django.contrib.auth import (
    login, authenticate,
    get_user_model
)
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import (
    View, TemplateView,
    ListView, DetailView,
    CreateView, UpdateView, DeleteView
)

from .forms import SignUpForm

User = get_user_model()

class WelcomeView(TemplateView):
    template_name = 'welcome.html'
    # https://teamtreehouse.com/library/templateview
    def get_context_data(self, **kwargs):
        user = self.request.user
        context = super().get_context_data(**kwargs)
        context["authenticated"] = user.is_authenticated
        context["username"] = user.username
        return context

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
    events = Event.objects.filter(creator=request.user)
    invitations = request.user.invited_events.all()
    invitation_count = request.user.invited_events.all().count()
    event_count = events.count()
    to_rsvps = None
    if Rsvp.objects.filter(invitee=request.user).exists():
        to_rsvps = Rsvp.objects.filter(invitee=request.user)
    return render(request, 'users/user_profile.html', {'events': events, 'event_count': event_count, 'invitations': invitations, 'invitation_count': invitation_count, 'to_rsvps': to_rsvps})

class EventDetailView(DetailView):
    model = Event

class EventCreateView(CreateView):
    model = Event
    fields = ("title", "description", "address", "start_time", "end_time", "invitees")

    def form_valid(self, form):
        user = self.request.user
        new_event = form.save(commit=False)
        new_event.creator = user
        new_event.save()
        print(new_event.invitees)
        return HttpResponseRedirect(self.get_success_url())

class EventView(DetailView):
    True

    # def event(request, pk):
    #     event = Event.objects.get(pk=pk)
    #     invitation_count = event.invitees.all().count()
    #     invitees = event.invitees.all()
    #     confirmed_yes = Rsvp.objects.all().filter(event=event, is_attending=True)
    #     user = request.user
    #     creator = event.is_creator(user)
    #     invitee_rsvp = None
    #     for invitee in invitees:
    #         if invitee.pk == user.pk:
    #             invitee_rsvp = Rsvp.objects.get(invitee=request.user, event=event)
    #     return render(request, 'events/event.html', {'event': event, 'invitation_count': invitation_count, 'invitees': invitees, 'is_creator': creator, 'invitee_rsvp': invitee_rsvp, 'confirmed_yes': confirmed_yes})
    #
    # @login_required
    # def event_destroy(request, pk):
    #     event = get_object_or_404(Event, pk=pk)
    #     event.delete()
    #     return redirect('user_profile', request.user.pk)

class RsvpView(View):
    @login_required
    def rsvp_edit(request, pk):
        rsvp = get_object_or_404(Rsvp, pk=pk)
        event = rsvp.event
        if request.method == "POST":
            form = RsvpEditForm(request.POST, instance=rsvp)
            if form.is_valid():
                rsvp_update = form.save(commit=False)
                rsvp_update.save()
                return redirect('event', pk=event.pk)
        else:
            form = RsvpEditForm(instance=rsvp)
            return render(request, 'events/rsvp_edit.html', {'form': form, 'event':event})
