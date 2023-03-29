from django.shortcuts import render
from django import forms
from django.contrib.auth import login, authenticate, logout  
from django.contrib import messages
from django.http import HttpResponseRedirect
from .models import CustomUser
# Create your views here.

class RegisterForm(forms.ModelForm):

    password1 = forms.CharField(widget=forms.PasswordInput(attrs={}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={}))

    class Meta:
        model = CustomUser
        fields = ['email', 'is_influencer','username']
        
    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError('Passwords do not match')
        return password2
    def save(self, commit=True): 
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        user.is_active = True
        user.save()
        return user
def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            return HttpResponseRedirect('/')
        
        else:
            if form.errors:
                for field in form:
                    for error in field.errors:
                        messages.error(request, error)
            print("ERROR")
    
    form = RegisterForm()
    
    context = {
        'form' : form
    }
    return render(request=request,template_name='registration/register.html',context=context)





class LoginForm(forms.Form):
    email = forms.CharField(max_length=255,required=True,widget=forms.EmailInput)
    password = forms.CharField(max_length=255,required=True,widget=forms.PasswordInput)

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(request,email=form.cleaned_data['email'], password=form.cleaned_data['password'])
            if user is not None:
                login(request=request,user=user)
                print(f'Succesfully logged in user {user}')
                return HttpResponseRedirect('/')
            else:
                messages.error(request=request,message='Password or email is incorrect!')            
    else:
        form = LoginForm()
    return render(request=request,template_name="registration/login.html",context={'form':form})


def logout_view(request):
    if(request.user.is_authenticated):
        logout(request)
    return HttpResponseRedirect('/')
