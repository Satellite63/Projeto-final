from django.contrib.auth import login, logout
from django.contrib.auth.hashers import check_password
from django.shortcuts import render, redirect
from django.contrib import messages
from db_utils import execute_sql
from django.contrib.auth import get_user_model

def sql_authenticate(username, password):
    # Consulta SQL direta para buscar o usuário
    query = """
    SELECT id_usuario, nome_usuario,senha_usuario
    FROM usuario
    WHERE nome_usuario = %s
    AND senha_usuario = %s
    """
    user_data = execute_sql(query, [username, password], True)
    if user_data:
        user_id, db_username, db_password = user_data
        if password == db_password:
            return {
                'id': user_id,
                'username': db_username,
                'password': db_password
            }
    # Verifica a senha (Django armazena senhas com hash)
    return None

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        #verifica se o usuario existe
        if sql_authenticate(username, password):
            user_data = sql_authenticate(username, password)
            #inciar sessão
            request.session['id_usuario'] = user_data['id']
            request.session['nome_usuario'] = user_data['username']
            request.session['verificaLogado'] = True
            request.session.set_expiry(3600)
            return redirect('home')
        
        messages.error(request, "Usuário ou senha incorretos!")
    
    return redirect('login')

def logout_view(request):
    request.session.flush()
    return redirect('home')