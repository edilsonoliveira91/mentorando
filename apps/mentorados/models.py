from django.db import models
from django.contrib.auth.models import User
from datetime import timedelta


class Navigators(models.Model):
  nome = models.CharField(max_length=200)
  user = models.ForeignKey(User, on_delete=models.CASCADE) #Mentor

  def __str__(self):
    return self.nome


class Mentorados(models.Model):
  estagio_choices = (
    ('E1', '10-100k'),
    ('E2', '100-1kk'),
  )
  nome = models.CharField(max_length=200)
  foto = models.ImageField(upload_to='fotos', null=True, blank=True)
  estagio = models.CharField(max_length=2, choices=estagio_choices)
  navigator = models.ForeignKey(Navigators, null=True, blank=True, on_delete=models.CASCADE)
  user = models.ForeignKey(User, on_delete=models.CASCADE) #Mentor
  criado_em = models.DateField(auto_now_add=True)

  def __str__(self):
    return self.nome


class DisponibilidadedeHorarios(models.Model):
  data_inicial = models.DateTimeField(null=True, blank=True)
  mentor = models.ForeignKey(User, on_delete=models.CASCADE)
  agendado = models.BooleanField(default=False)

  def data_final(self):
    return self.data_inicial + timedelta(minutes=50)