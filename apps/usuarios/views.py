from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.messages import constants
from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib import auth


def cadastro(request):
  if request.method == 'GET':
    return render(request, 'cadastro.html')
  elif request.method == 'POST':
    username = request.POST.get('username')
    senha = request.POST.get('senha')
    confirmar_senha = request.POST.get('confirmar_senha')

    if senha != confirmar_senha:
      messages.add_message(request, constants.ERROR, 'Senha e confirmar senha devem ser iguais!')
      return redirect('cadastro')
    
    if len(senha) < 6:
      messages.add_message(request, constants.ERROR, 'Senha deve ter 6 ou mais caracteres!')
      return redirect('cadastro')
    
    users = User.objects.filter(username=username)
    if users.exists():
      messages.add_message(request, constants.ERROR, 'Usuario já existente!')
      return redirect('cadastro')
    
  
    User.objects.create_user(
      username=username,
      password=senha
    )

    return redirect('login')


def login(request):
  if request.method == 'GET':
    return render(request, 'login.html')
  elif request.method == 'POST':
    username = request.POST.get('username')
    senha = request.POST.get('senha')

    user = authenticate(request, username=username, password=senha)

    if user:
      auth.login(request, user)
      return redirect('/mentorados/')
    
    messages.add_message(request, constants.ERROR, 'Usuario ou senha invalidos!')
    return redirect('login')
  

def logout(request):
  auth.logout(request)
  return redirect('login')

