from django.shortcuts import render, redirect
from rack.views import listar_racks

def home(request):
    if not request.session.get('verificaLogado'):
        return redirect('login')
    return render(request, 'tela_inicial.html')

def login(request):
    return render(request, 'index.html')

def rack(request):
    #print(listar_racks(request))
    return render(request, 'rack.html', {'racks': listar_racks(request) })

def addhidro(request):
    return render(request, 'addhidro.html')

def estoque(request):
    return render(request, 'estoque.html')

def monitoramento(request):
    return render(request, 'monitoramento.html')

def caixa(request):
    return render(request, 'caixa.html')

def retornaHome(request):
    return render(request, 'tela_inicial.html')