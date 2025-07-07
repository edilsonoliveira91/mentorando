from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404
from .models import Mentorados, Navigators, DisponibilidadedeHorarios
from django.contrib import messages
from django.contrib.messages import constants
from datetime import datetime, timedelta


def mentorados(request):
  if not request.user.is_authenticated:
    return redirect('login')
  
  if request.method == 'GET':
    navigators = Navigators.objects.filter(user=request.user)
    mentorados = Mentorados.objects.filter(user=request.user)

    estagios_flat = []
    for i in Mentorados.estagio_choices:
      estagios_flat.append(i[1])
    qtd_estagios = []
    for i, j in Mentorados.estagio_choices:
      quantidade = Mentorados.objects.filter(estagio=i).filter(user=request.user).count()
      qtd_estagios.append(quantidade)
    print(estagios_flat)
    print(qtd_estagios)



    return render(request, 'mentorados.html', {'estagios': Mentorados.estagio_choices, 'navigators': navigators, 'mentorados': mentorados, 'estagios_flat': estagios_flat, 'qtd_estagios': qtd_estagios})
  
  elif request.method == 'POST':
    nome = request.POST.get('nome')
    foto = request.FILES.get('foto')
    estagio = request.POST.get('estagio')
    navigator = request.POST.get('navigator')

    mentorado = Mentorados(
      nome=nome,
      foto=foto,
      estagio=estagio,
      navigator_id=navigator,
      user=request.user
    )

    mentorado.save()
    messages.add_message(request, constants.SUCCESS, 'Mentorado cadastrado com sucesso!')
    return redirect('mentorados')
  

def reunioes(request):
  if request.method == 'GET':
    return render(request, 'reunioes.html')
  elif request.method == 'POST':
    data = request.POST.get('data')
    data = datetime.strptime(data, '%Y-%m-%dT%H:%M')

    disponibilidades = DisponibilidadedeHorarios.objects.filter(mentor=request.user).filter(
      data_inicial__gte=(data - timedelta(minutes=50)), # __ gte  maior ou igual 
      data_inicial__lte=(data + timedelta(minutes=50)), # __lte menor ou igual
    )

    if disponibilidades.exists():
      messages.add_message(request, constants.ERROR, 'Você já possui uma reunião em aberto!')
      return redirect('reunioes')
    
    if data < datetime.now():
      messages.add_message(request, constants.ERROR, 'A data selecionada é menor que a data de hoje!')
      return redirect('reunioes')

    disponibilidades = DisponibilidadedeHorarios(
      data_inicial=data,
      mentor=request.user
    )

    disponibilidades.save()
    messages.add_message(request, constants.SUCCESS, 'Agendamento realizado com sucesso!')
    return redirect('reunioes')
  

def auth(request):
  if request.method == 'GET':
    return render(request, 'auth_mentorado.html')
  elif request.method == 'POST':
    token = request.POST.get('token')

    if not Mentorados.objects.filter(token=token).exist():
      messages.add_message(request, constants.ERROR, 'Token inválido!')
      return redirect('auth_mentorado')
    
    response = redirect('escolher_dia')
    response.set_cookie('auth_token', token, max_age=3600)

    return response
