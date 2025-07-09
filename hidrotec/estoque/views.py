from django.shortcuts import render, redirect 
from db_utils import execute_sql
from django.contrib import messages

# Função para inserir um novo estoque no banco de dados
def inserir_estoque(categoria, fornecedor, dt_validade_estoque, dt_entrada_estoque, descricao, tipo_despesa, id_add_hidro, quantidade_estoque, nome_estoque, valor_estoque):
    try:
        # Query SQL para inserção do estoque
        sql = """
        INSERT INTO estoque(
            categoria, fornecedor, dt_validade_estoque, dt_entrada_estoque, descricao, tipo_despesa, id_add_hidro, quantidade_estoque, nome_estoque, valor_estoque)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    
        """
        # Executa a query com os parâmetros e fetch=True para obter resultado
        execute_sql(sql, [categoria, fornecedor, dt_validade_estoque, dt_entrada_estoque, descricao, tipo_despesa, id_add_hidro, quantidade_estoque, nome_estoque, valor_estoque], False)
        
    except Exception as e:
        print(f"Erro ao inserir no estoque: {str(e)}")
        return None
    
# Função para editar um estoque existente
def editar_estoque(id, categoria, fornecedor, dt_validade_estoque, dt_entrada_estoque, descricao, tipo_despesa, id_add_hidro, quantidade_estoque, nome_estoque, valor_estoque):
        # Query SQL para atualização do estoque
        sql = """
        UPDATE public.estoque
        SET categoria=%s, fornecedor=%s, dt_validade_estoque=%s, dt_entrada_estoque=%s, descricao=%s, id_add_hidro=%s, quantidade_estoque=%s, nome_estoque=%s, valor_estoque=%s
        WHERE id_estoque=%s;
        """
        # Executa a query com os parâmetros
        execute_sql(sql, [categoria, fornecedor, dt_validade_estoque, dt_entrada_estoque, descricao, id_add_hidro, quantidade_estoque, nome_estoque, valor_estoque, id], False)
       
        
# Função para remover um estoque
def remover_estoque(id):
    try:
        # Query SQL para deletar o estoque
        sql = """
        DELETE FROM public.estoque
        WHERE id_estoque = %s;
        """
        # Executa a query
        estoque = execute_sql(sql, [id], True)
        return True  # Retorna True indicando sucesso
        
    except Exception as e:
        print(f"Erro ao remover estoque: {str(e)}")  
        return None

# View para processar o formulário de criação de estoque
def formulario_estoque(request): 
    if request.method == 'POST':  # Verifica se é uma requisição POST
        print("Formulário de estoque recebido") 
        
        # Obtém dados do formulário
        categoria = request.POST.get('categoria')
        fornecedor = request.POST.get('fornecedor')
        dt_validade_estoque = request.POST.get('dt_validade_estoque')
        dt_entrada_estoque = request.POST.get('dt_entrada_estoque')
        descricao = request.POST.get('descricao')
        tipo_despesa = request.POST.get('tipo_despesa')
        id_add_hidro = request.POST.get('plantio')
        quantidade_estoque = request.POST.get('quantidade')
        nome_estoque = request.POST.get('nome_estoque')
        valor_estoque = request.POST.get('valor_estoque')

        try:
            # Chama função para inserir estoque
            estoque_id = inserir_estoque(categoria, fornecedor, dt_validade_estoque, dt_entrada_estoque, descricao, tipo_despesa, id_add_hidro, quantidade_estoque, nome_estoque, valor_estoque)
        
            messages.success(request, "Estoque cadastrado com sucesso!")
            return redirect('../estoque/')

        except ValueError as e:
            messages.error(request, f"Quantidade deve ser um número válido: {str(e)}")
        except Exception as e:
            messages.error(request, f"Erro no sistema: {str(e)}")
    
    # Redireciona para a página de estoque em caso de GET ou erro
    return redirect('../estoque/')

# View para processar o formulário de edição de estoque
def formulario_estoque_edit(request): 
    if request.method == 'POST': 
        print("Formulário de edição estoque recebido") 
        
        # Obtém dados do formulário
        id = request.POST.get('estoque_id')
        categoria = request.POST.get('novaCategoria')
        fornecedor = request.POST.get('novoFornecedor')
        dt_validade_estoque = request.POST.get('novaDt_validade_estoque')
        dt_entrada_estoque = request.POST.get('novaDt_entrada_estoque')
        descricao = request.POST.get('novaDescricao')
        tipo_despesa = request.POST.get('novoTipo_despesa')
        id_add_hidro = request.POST.get('novoPlantio')
        quantidade_estoque = request.POST.get('novaQuantidade_estoque')
        nome_estoque = request.POST.get('novoNome_estoque')
        valor_estoque = request.POST.get('novoValor_estoque')

        try:
            # Chama função para editar estoque
            sucesso = editar_estoque(id, categoria, fornecedor, dt_validade_estoque, dt_entrada_estoque, descricao, tipo_despesa, id_add_hidro, quantidade_estoque, nome_estoque, valor_estoque)
            
            return redirect('../estoque/')
                
        except ValueError as e:
            messages.error(request, f"Quantidade deve ser um número válido: {str(e)}")
        except Exception as e:
            messages.error(request, f"Erro no sistema: {str(e)}")
    
    return redirect('../estoque/')

# View para processar o formulário de remoção de estoque
def formulario_estoque_remove(request): 
    if request.method == 'POST': 
        print("Formulário de eliminação estoque recebido") 
        
        # Obtém ID do estoque a ser removido
        id = request.POST.get('estoque_id')
        
        # Chama função para remover estoque
        sucesso = remover_estoque(id)
        
        messages.success(request, "Estoque removido com sucesso")

    return redirect('../estoque/')

# Função para listar estoque com possíveis filtros
def listar_estoque(request):
    # Query base
    query = """
    SELECT id_estoque, nome_estoque, categoria, quantidade_estoque, valor_estoque, dt_entrada_estoque, dt_validade_estoque, fornecedor, descricao
    FROM estoque
    WHERE 1=1  
    """
    
    params = []  # Lista para parâmetros da query
    
    # Filtro por termo de busca
    q = request.GET.get('q')
    
    if q:
        query += " AND (nome_estoque LIKE %s)"  # Filtra por nome
        params.extend([f'%{q}%'])  # Adiciona parâmetro com wildcards
    
    # Ordenação padrão
    query += " ORDER BY nome_estoque"
    
    # Executa a query e retorna resultados
    estoque_paginados = execute_sql(query, params, False)
    return estoque_paginados

# View para logout
def logout_view(request):
    request.session.flush()  # Limpa toda a sessão
    return redirect('home')  # Redireciona para a página inicial

