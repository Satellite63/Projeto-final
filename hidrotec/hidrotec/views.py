from django.shortcuts import render, redirect
from rack.views import listar_racks
from addhidro.views import listar_hidro
from estoque.views import listar_estoque
from monitoramento.views import dashboard_estoque, gerar_grafico_tipo

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
    return render(request, 'addhidro.html', {'hidros': listar_hidro(request)})

def estoque(request):
    return render(request, 'estoque.html', {'estoques': listar_estoque(request)})

def monitoramento(request):
    return render(request, 'monitoramento.html', {'dados': dashboard_estoque(), 'dadosjs': gerar_grafico_tipo()})

def caixa(request):
    return render(request, 'caixa.html')

def retornaHome(request):
    return render(request, 'tela_inicial.html')