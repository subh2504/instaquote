from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic
from .forms import SignUpForm
from django.contrib.auth import login, authenticate


class SignUp(generic.CreateView):
    form_class = SignUpForm
    success_url = reverse_lazy('quotes:list')
    template_name = 'registration/signup.html'
    
    def form_valid(self, form):
        valid = super(SignUp, self).form_valid(form)
        username, password = form.cleaned_data.get('username'), form.cleaned_data.get('password1')
        new_user = authenticate(username=username, password=password)
        login(self.request, new_user)
        return valid