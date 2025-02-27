from django.shortcuts import render
from .models import Topic
from .forms import TopicForm
from django.http import HttpResponseRedirect
from django.urls import reverse
# Create your views here.

def index(request):
    """Página princiapl do learning log"""
    return render(request, 'learning_logs/index.html')

def topics(request):
    """Mostra todos os assunto"""
    topics = Topic.objects.order_by('date_added')
    context = {'topics': topics}
    return render(request,'learning_logs/topics.html', context)

def topic(request, topic_id):
    """Mostra um unico assunto com todas as suas entradas"""
    topic = Topic.objects.get(id = topic_id)
    entries = topic.entry_set.order_by('-date_added')
    context = {'topic': topic, 'entries': entries}
    return render(request, 'learning_logs/topic.html', context)


def new_topic (request):
    """Adiciona um novo assunto """
    if request.method != 'POST':
        #Nenhum dado submetido; cria um formulario em branco

        form = TopicForm()
    else:
        #dados de POST submetidos; processa os dados
        form = TopicForm (request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('topics'))
    
    context = {'form': form}
    return render(request, 'learning_logs/new_topic.html', context)