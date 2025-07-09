from django.shortcuts import render, redirect 
from db_utils import execute_sql
from django.contrib import messages

# Função para inserir uma nova planta no banco de dados
def inserir_hidro(nome, quantidade, valor, dt_plantio, dt_colheita):
    try:
        # Query SQL para inserção da planta
        sql = """
        INSERT INTO add_hidro(
            nome_hidro, quantidade_hidro, valor_hidro, dt_plantio_hidro, dt_colheita_hidro )
        VALUES (%s, %s, %s, %s, %s)
        RETURNING id_addhidro 
        """
        # Executa a query com os parâmetros e fetch=True para obter resultado
        execute_sql(sql, [nome, quantidade, float(valor), dt_plantio, dt_colheita], True)
        
        
    except Exception as e:
        print(f"Erro ao inserir na hidroponia: {str(e)}")
        return None
    
# Função para editar uma planta existente
def editar_hidro(id, nome, quantidade, valor, dt_plantio, dt_colheita):
    try:
        # Query SQL para atualização da planta
        sql = """
        UPDATE public.add_hidro
        SET nome_hidro=%s, quantidade_hidro=%s, valor_hidro=%s, dt_plantio_hidro=%s, dt_colheita_hidro=%s
        WHERE id_addhidro = %s;
        """
        # Executa a query com os parâmetros
        hidro = execute_sql(sql, [nome, quantidade, valor, dt_plantio, dt_colheita, id], True)
        return True  # Retorna True indicando sucesso
        
    except Exception as e:
        print(f"{str(e)}")  
        return None

# Função para remover uma planta
def remover_hidro(id):
    try:
        # Query SQL para deletar a planta
        sql = """
        DELETE FROM public.add_hidro
        WHERE id_addhidro = %s;
        """
        # Executa a query
        hidro = execute_sql(sql, [id], True)
        return True  # Retorna True indicando sucesso
        
    except Exception as e:
        print(f"Erro ao remover de hidro: {str(e)}")
        return None

# View para processar o formulário de criação de planta
def formulario_hidro(request): 
    if request.method == 'POST':
        print("Formulário de hidro recebido") 
        
        # Obtém dados do formulário
        nome = request.POST.get('nomeHidro')
        quantidade = request.POST.get('quantidadeHidro')
        valor = request.POST.get('valor')
        dt_plantio = request.POST.get('dt_plantio')
        dt_colheita = request.POST.get('dt_colheita')
        

        try:
            # Converte quantidade para inteiro
            quantidade_int = int(quantidade)
            
            # Chama função para inserir planta
            hidro_id = inserir_hidro(nome, quantidade_int, valor, dt_plantio, dt_colheita)
            
            messages.success(request, "hidro cadastrada com sucesso!")
            return redirect('../addhidro/')
                
        except ValueError as e:
            messages.error(request, f"Quantidade deve ser um número válido: {str(e)}")
    
    # Redireciona para a página de plantas em caso de GET ou erro
    return redirect('../addhidro/')

# View para processar o formulário de edição de planta
def formulario_hidro_edit(request): 
    if request.method == 'POST': 
        print("Formulário de edição hidro recebido") 
        
        # Obtém dados do formulário
        id = request.POST.get('addhidro_id')
        nome = request.POST.get('novoNomeHidro')
        quantidade = request.POST.get('novoQuantidadeHidro')
        valor = request.POST.get('novoValor')
        dt_plantio = request.POST.get('novoDt_plantio')
        dt_colheita = request.POST.get('novoDt_colheita')
        


        try:
            # Chama função para editar planta
            sucesso = editar_hidro(id, nome, quantidade, valor, dt_plantio, dt_colheita)
            
            if sucesso:
                messages.success(request, "Hidro atualizada com sucesso!")
                return redirect('../addhidro/')
            else:
                messages.error(request, "")
                
        except ValueError as e:
            messages.error(request, f"Quantidade deve ser um número válido: {str(e)}")
        except Exception as e:
            messages.error(request, f"Erro no sistema: {str(e)}")
    
    return redirect('../addhidro/')

# View para processar o formulário de remoção de planta
def formulario_hidro_remove(request): 
    if request.method == 'POST': 
        print("Formulário de eliminação hidro recebido") 
        
        # Obtém ID da planta a ser removida
        id = request.POST.get('addhidro_id')
        
        # Chama função para remover planta
        sucesso = remover_hidro(id)
        
        messages.success(request, "hidro removida com sucesso")

    return redirect('../addhidro/')

# Função para listar plantas com possíveis filtros
def listar_hidro(request):
    # Query base
    query = """
    SELECT id_addhidro, nome_hidro, quantidade_hidro, valor_hidro, dt_plantio_hidro, dt_colheita_hidro 
    FROM add_hidro
    WHERE 1=1  
    """
    
    params = []  # Lista para parâmetros da query
    
    # Filtro por termo de busca
    q = request.GET.get('q')
    
    if q:
        query += " AND (nome_hidro LIKE %s)"  # Filtra por nome
        params.extend([f'%{q}%'])  # Adiciona parâmetro com wildcards
    
    # Ordenação padrão
    query += " ORDER BY nome_hidro"
    
    # Executa a query e retorna resultados
    hidro_paginadas = execute_sql(query, params, False)
    return hidro_paginadas

# View para logout (mantida igual)
def logout_view(request):
    request.session.flush()  # Limpa toda a sessão
    return redirect('home')  # Redireciona para a página inicial