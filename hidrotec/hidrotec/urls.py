from django.contrib import admin
from django.urls import path
import hidrotec .views
import usuario.views
import rack.views
import addhidro.views
import estoque.views
import monitoramento.views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',hidrotec.views.login, name='login'),
    path('home/', hidrotec.views.home, name='home'),
    path('autenticar/', usuario.views.login_view, name='autenticar'),
    path('sair/', usuario.views.logout_view, name='sair'),
    path('rack/', hidrotec.views.rack, name='rack'),
    path('addhidro/', hidrotec.views.addhidro, name='addhidro'),
    path('estoque/', hidrotec.views.estoque, name='estoque'),
    path('monitoramento/', hidrotec.views.monitoramento, name='monitoramento'),
    path('caixa/', hidrotec.views.caixa, name='caixa'),
    path('home2/', hidrotec.views.retornaHome, name='home2'),
    path('rack_form/', rack.views.formulario_rack, name='formularioRack'),
    path('rack_form_edit/', rack.views.formulario_rack_edit, name='formularioRackEdit'),
    path('rack_form_remove/', rack.views.formulario_rack_remove, name='formularioRackRemover'),
    path('hidro_form/', addhidro.views.formulario_hidro, name='formularioHidro'),
    path('hidro_form_edit/', addhidro.views.formulario_hidro_edit, name='formularioHidroEdit'),
    path('hidro_form_remove/', addhidro.views.formulario_hidro_remove, name='formularioHidroRemover'),
    path('estoque_form/', estoque.views.formulario_estoque, name='formularioEstoque'),
    path('estoque_form_edit/', estoque.views.formulario_estoque_edit, name='formularioEstoqueEdit'),
    path('estoque_form_remove/', estoque.views.formulario_estoque_remove, name='formularioEstoqueRemover'),
    path('dashboard-estoque/', monitoramento.views.dashboard_estoque, name='dashboard_estoque'),
 
    

]
