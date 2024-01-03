from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.urls import reverse
from authentication.utils import valid_inputs, blank_username
from authentication.models import CustomUser, Token
from authentication.tasks import token_and_mail
from django.contrib import messages
from django.contrib.messages import constants

def login(request):
    return HttpResponse('login')

def register(request):
    if request.method == "GET":
        return render(request, 'register.html')
    
    elif request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm-password')

        #Faz a verficiação da string username e retorna ela modificada caso precise
        result, username_modified = blank_username(request, username)

        if not result:
            return redirect(reverse('register'))

        elif not valid_inputs(request, username_modified, email, password, confirm_password):
            return redirect(reverse('register'))
        
        else:
            try:
                user = CustomUser.objects.create(
                    username=username_modified,
                    email=email,
                    password=password
                )
                
                token_and_mail(user)

                return render(request, 'token_confirm.html')
            except:
                messages.add_message(request, constants.ERROR, 'Erro interno: Por favor, contate um administrador.')
                return redirect(reverse('register'))

def active_token(request, token):
    if request.method == "GET":
        token = Token.objects.get(token=token)
        token.user.is_active = True
        token.active = True

        token.save()
