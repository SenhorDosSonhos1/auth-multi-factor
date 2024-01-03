from django.contrib.messages import constants
from django.contrib import messages
import re

def blank_username(request, string):
    string = string.strip()
    #Verifica se contem espaço vazio e se maior q 1 ele da erro senao ele coloca um underscore
    if string.count(' ') > 1:
        messages.add_message(request, 'O username não pode conter mais de 1(_) espaços em brancos')
        return False, None
    #Aceitar numeros inteiros somente apos letras
    pattern = re.compile(r'[a-zA-Z]+[0-9]+$')
    #Se o padrão de numeros inteiros apos a letra for atinjido ele transforma espaço em branco dentro da string em undescore(caso exista)
    if pattern.search(string):
        modified_string = string.replace(' ', '_')
        return True, modified_string
    else:
        messages.add_message(request, constants.ERROR, 'O username precisa ter pelo menos uma letra seguida por números inteiros.')
        return False, None
    
def valid_inputs(request, username, email, password, confirm_password):
    if len(username) < 3:
        messages.add_message(request, constants.ERROR, 'O username precisa ter pelo menos 3 caracteres.')
        return False
    
    elif len(username) > 16:
        messages.add_message(request, constants.ERROR, 'O username precisa ter no máximo 16 caracteres.')
        return False

    elif email.count() >= 1:
        messages.add_message(request, constants.ERROR, 'O E-mail não pode conter espaços em brancos.')
        return False
    
    elif len(password) < 6 and len(password) > 16:
        messages.add_message(request, constants.ERROR, 'A senha precisater pelo menos 6 caracteres e no máximo 16.')
        return False
    
    elif re.search(r'[a-z]', password):
        messages.add_message(request, constants.ERROR, 'A senha precisa ter pelos menos uma letra maiscula')
        return False
    
    elif re.search(r'[A-Z]', password):
        messages.add_message(request, constants.ERROR, 'A senha precisa ter pelos menos uma minuscula.')
        return False
    
    elif re.search(r'[0-9]', password):
        messages.add_message(request, constants.ERROR, 'A senha precisa ter pelos menos um numero inteiro.')
        return False
    
    elif re.search(r'[#&@%]', password):
        messages.add_message(request, constants.ERROR, 'A senha precisa ter pelos menos uma e pelo menos um desses caracteres especiaais (#@$&%).')
        return False
    
    elif password != confirm_password:
        messages.add_message(request, constants.ERROR, 'As senhas não podem ser diferentes.')
        return False

    return True