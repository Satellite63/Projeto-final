from django.shortcuts import render, redirect 
from db_utils import execute_sql
from django.contrib import messages

# Função para inserir um novo rack no banco de dados
def inserir_rack(nome, quantidade):
    try:
        # Query SQL para inserção do rack
        sql = """
        INSERT INTO rack(
            nome_rack, quantidade_rack)
        VALUES (%s, %s)
        RETURNING id_rack 
        """
        # Executa a query com os parâmetros e fetch=True para obter resultado
        rack = execute_sql(sql, [nome, quantidade], True)
        
        if rack:
            return rack[0]  # Retorna o ID do rack inserido (primeira coluna do primeiro registro)
        return None
        
    except Exception as e:
        print(f"Erro ao inserir rack: {str(e)}")
        return None
    
# Função para editar um rack existente
def editar_rack(id, nome, quantidade):
    try:
        # Query SQL para atualização do rack
        sql = """
        UPDATE public.rack
        SET nome_rack=%s, quantidade_rack=%s
        WHERE id_rack = %s;
        """
        # Executa a query com os parâmetros
        rack = execute_sql(sql, [nome, quantidade, id], True)
        return True  # Retorna True indicando sucesso
        
    except Exception as e:
        print(f"Erro ao editar rack: {str(e)}")  
        return None

# Função para remover um rack
def remover_rack(id):
    try:
        # Query SQL para deletar o rack
        sql = """
        DELETE FROM public.rack
        WHERE id_rack = %s;
        """
        # Executa a query
        rack = execute_sql(sql, [id], True)
        return True  # Retorna True indicando sucesso
        
    except Exception as e:
        print(f"Erro ao remover rack: {str(e)}")  # Mensagem corrigida de "inserir" para "remover"
        return None

# View para processar o formulário de criação de rack
def formulario_rack(request): 
    if request.method == 'POST':  # Verifica se é uma requisição POST
        print("Formulário de rack recebido") 
        
        # Obtém dados do formulário
        nome = request.POST.get('nomeRack')
        quantidade = request.POST.get('quantidadeRack')

        # Valida campos obrigatórios
        if not all([nome, quantidade]):
            messages.error(request, "Preencha todos os campos obrigatórios")
            return redirect('./rack/')

        try:
            # Converte quantidade para inteiro
            quantidade_int = int(quantidade)
            
            # Chama função para inserir rack
            rack_id = inserir_rack(nome, quantidade_int)
            
            if rack_id:
                messages.success(request, "Rack cadastrado com sucesso!")
                return redirect('../rack/')
            else:
                messages.error(request, "Erro ao cadastrar rack")
                
        except ValueError as e:
            messages.error(request, f"Quantidade deve ser um número válido: {str(e)}")
        except Exception as e:
            messages.error(request, f"Erro no sistema: {str(e)}")
    
    # Redireciona para a página de racks em caso de GET ou erro
    return redirect('../rack/')

# View para processar o formulário de edição de rack
def formulario_rack_edit(request): 
    if request.method == 'POST': 
        print("Formulário de edição rack recebido") 
        
        # Obtém dados do formulário
        id = request.POST.get('rack_id')
        nome = request.POST.get('novoNomeRack')
        quantidade = request.POST.get('novaQuantidadeRack')

        try:
            # Chama função para editar rack
            sucesso = editar_rack(id, nome, quantidade)
            
            if sucesso:
                messages.success(request, "Rack atualizado com sucesso!")
                return redirect('../rack/')
            else:
                messages.error(request, "Erro ao atualizar rack")
                
        except ValueError as e:
            messages.error(request, f"Quantidade deve ser um número válido: {str(e)}")
        except Exception as e:
            messages.error(request, f"Erro no sistema: {str(e)}")
    
    return redirect('../rack/')

# View para processar o formulário de remoção de rack
def formulario_rack_remove(request): 
    if request.method == 'POST': 
        print("Formulário de eliminação rack recebido") 
        
        # Obtém ID do rack a ser removido
        id = request.POST.get('rack_id')
        
        # Chama função para remover rack
        sucesso = remover_rack(id)
        
        if sucesso:
            messages.success(request, "Rack removido com sucesso")
        else:
            messages.error(request, "Erro ao remover rack")

    return redirect('../rack/')

# Função para listar racks com possíveis filtros
def listar_racks(request):
    # Query base
    query = """
    SELECT id_rack, nome_rack, quantidade_rack
    FROM rack
    WHERE 1=1  
    """
    
    params = []  # Lista para parâmetros da query
    
    # Filtro por termo de busca
    q = request.GET.get('q')
    
    if q:
        query += " AND (nome_rack LIKE %s)"  # Filtra por nome
        params.extend([f'%{q}%'])  # Adiciona parâmetro com wildcards
    
    # Ordenação padrão
    query += " ORDER BY nome_rack"
    
    # Executa a query e retorna resultados
    racks_paginados = execute_sql(query, params, False)
    return racks_paginados

# View para logout
def logout_view(request):
    request.session.flush()  # Limpa toda a sessão
    return redirect('home')  # Redireciona para a página inicial