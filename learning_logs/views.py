from django.shortcuts import render
from .models import Topic,Entry
from .forms import TopicForm,EntryForm
from django.http import HttpResponseRedirect,Http404
from django.urls import reverse
from django.contrib.auth.decorators import login_required


def index(request):
    """Página princiapl do learning log"""
    return render(request, 'learning_logs/index.html')

@login_required
def topics(request):
    """Mostra todos os assunto"""
    topics = Topic.objects.filter(owern=request.user).order_by('date_added')
    context = {'topics': topics}
    return render(request,'learning_logs/topics.html', context)

@login_required
def topic(request, topic_id):
    """Mostra um unico assunto com todas as suas entradas"""
    topic = Topic.objects.get(id = topic_id)
    
    # Garanti que o assunto perntenca ao usario atual
    if topic.owern != request.user:
        raise Http404
    
    entries = topic.entry_set.order_by('-date_added')
    context = {'topic': topic, 'entries': entries}
    return render(request, 'learning_logs/topic.html', context)

@login_required
def new_topic (request):
    """Adiciona um novo assunto """
    if request.method != 'POST':
        #Nenhum dado submetido; cria um formulario em branco

        form = TopicForm()
    else:
        #dados de POST submetidos; processa os dados
        form = TopicForm (request.POST)
        if form.is_valid():
            new_topic = form.save(commit=False)
            new_topic.owern = request.user
            new_topic.save()
            return HttpResponseRedirect(reverse('topics'))
    
    context = {'form': form}
    return render(request, 'learning_logs/new_topic.html', context)

@login_required
def new_entry(request, topic_id):
    """Acrescenta um anova entrada para um assunto em particular"""
    topic = Topic.objects.get(id = topic_id)
    if topic.owern != request.user:
        raise Http404


    if request.method != 'POST' :
        #Nenhum dado submetido; cria um formulario em branco
        form = EntryForm()

    else:
        #Dados de POST submetidos processa os dados
        form = EntryForm(data=request.POST)
        if form.is_valid():
            new_entry = form.save(commit=False)
            new_entry.topic = topic
            new_entry.save()
            return HttpResponseRedirect(reverse('topic', args=[topic_id]))
    
    context = {'topic': topic, 'form': form}
    return render(request, 'learning_logs/new_entry.html', context)

@login_required
def edit_entry (request, entry_id):
    """Edita uma entrada existente"""
    entry = Entry.objects.get(id=entry_id)
    topic = entry.topic

    if topic.owern != request.user:
        raise Http404

    if request.method != 'POST':
        # Requisição incial; preenche brevimnete o fomulário com a entrada atual
        form = EntryForm(instance=entry)

    else:
        #Dados de POST submetidos; processa os dados
        form = EntryForm(instance=entry, data=request.POST)
        if form.is_valid():
            form.save()
        return HttpResponseRedirect(reverse('topic', args=[topic.id]))
    
    context = {'entry': entry, 'topic': topic, 'form': form}
    
    return render(request, 'learning_logs/edit_entry.html', context)