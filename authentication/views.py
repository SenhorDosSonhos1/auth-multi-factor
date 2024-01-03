from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.urls import reverse
from authentication.utils import valid_inputs, blank_username
from authentication.models import CustomUser, Token
from authentication.tasks import token_and_mail
from django.contrib import messages
from django.contrib.messages import constants

def login(request):
    return render(request, 'login.html')

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
        
        elif CustomUser.objects.filter(email=email).exists():
            messages.add_message(request, constants.ERROR, 'Esse usuario já existe')
            return redirect(reverse('register'))
        else:
            try:
                user = CustomUser.objects.create_user(
                    username=username_modified,
                    email=email,
                    password=password
                )

                token = token_and_mail.delay(user.id)

                messages.add_message(request, messages.INFO, 'Por favor, confirme seu e-mail através do link enviado.')
                return redirect(reverse('login'))
            
            except Exception as e:
                print(f"Error: {e}")
                messages.add_message(request, constants.ERROR, 'Erro interno: Por favor, contate um administrador.')
                return redirect(reverse('register'))

def active_token(request, token):
    if request.method == "GET":
        token = get_object_or_404(Token, token=token)
        token.user.is_active = True
        token.active = True

        token.user.save()
        token.save()

        messages.add_message(request, constants.SUCCESS, 'Conta ativada com sucesso.')
        return redirect(reverse('login'))