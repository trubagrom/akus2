from django.contrib.auth import authenticate
from django.contrib.auth.views import LoginView
from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from .utils import *
from .models import *
from .forms import *
from django.http import HttpResponseRedirect


def greet(request):
    return render(request, 'main/greet.html')


@login_required
def mainpage(request):
    u = User.objects.get(username=request.user.username)
    # instruments = Instruments.objects.all()
    # my_bands_vacations = BandVacanction.objects.filter(person=u)
    others_bands_vacations = BandVacanction.objects.exclude(person=u)
    my_skills = [x.id for x in UserInstuments.objects.get(user=u).instrument.all()]
    applicable_band_vacations = []
    idx = 0
    for bv in others_bands_vacations:
        if bv.instrument.id in my_skills:
            bv.card_idx = idx
            idx += 1
            applicable_band_vacations.append(bv)

    return render(request, 'main/mainpage.html', {
        'applicable_band_vacations': applicable_band_vacations,
        'max_card_idx': idx-1,
    })


@login_required
def create_new_band(request):
    if request.method == "POST":
        if "add" in request.POST:
            b = Band()
            b.name = request.POST["name"]
            b.link = request.POST.get("link", "")
            b.about = request.POST.get("about", "")
            b.save()
            idx = 1
            while f"instrument_{idx}" in request.POST:
                bv = BandVacanction()
                bv.band = b
                bv.instrument = Instruments.objects.get(id=request.POST[f"instrument_{idx}"])
                bv.save()
                idx += 1
    return HttpResponseRedirect(reverse_lazy("main"))


@login_required
def update_band(request):
    if request.method == "POST":
        if "update" in request.POST:
            u = User.objects.get(username=request.user.username)
            bvs = request.POST.getlist('bvs[]')
            for bv in bvs:
                bvo = BandVacanction.objects.get(id=bv)
                bvo.person = u
                bvo.save()
    return HttpResponseRedirect(reverse_lazy("manage_bands"))


@login_required
def update_band_get(request, vacation_id):
    u = User.objects.get(username=request.user.username)
    bvo = BandVacanction.objects.get(id=vacation_id)
    bvo.person = u
    bvo.save()
    return HttpResponseRedirect(reverse_lazy("manage_bands"))


@login_required
def manage_skills(request):
    u = User.objects.get(username=request.user.username)
    instruments = Instruments.objects.all()

    if request.method == 'POST':
        us = UserInstuments.objects.get(user=u)
        rp = request.POST
        new_skills = request.POST.getlist("skills[]")
        new_skills = [int(i) for i in new_skills]
        for i in instruments:
            if i.id in new_skills:
                us.instrument.add(i)
            else:
                us.instrument.remove(i)

        return HttpResponseRedirect(reverse_lazy("manage_skills"))
    my_skills = [x.id for x in UserInstuments.objects.get(user=u).instrument.all()]

    for i in instruments:
        if i.id in my_skills:
            i.checked = True
        else:
            i.checked = False
    return render(request, 'main/skills.html',  {
        'instruments': instruments,

    })


@login_required
def manage_bands(request):
    u = User.objects.get(username=request.user.username)
    instruments = Instruments.objects.all()
    my_bands_vacations = BandVacanction.objects.filter(person=u)
    others_bands_vacations = BandVacanction.objects.exclude(person=u)
    my_skills = [x.id for x in UserInstuments.objects.get(user=u).instrument.all()]
    applicable_band_vacations = []
    for bv in others_bands_vacations:
        if bv.instrument.id in my_skills:
            applicable_band_vacations.append(bv)
    return render(request, 'main/bands.html',  {
        'my_bands_vacations': my_bands_vacations,
        'applicable_band_vacations': applicable_band_vacations,
        'instruments': instruments,

    })


class RegisterUser(DataMixin, CreateView):
    form_class = UserCreationForm
    template_name = 'main/registration.html'
    success_url = reverse_lazy('login')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Регистрация")
        return dict(list(context.items()) + list(c_def.items()))

    def get_success_url(self):
        return reverse_lazy('log')


class LoginUser(DataMixin, LoginView):
    form_class = LoginUserForm
    template_name = 'main/log.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Авторизация")
        return dict(list(context.items()) + list(c_def.items()))

    def get_success_url(self):
        return reverse_lazy('main')




