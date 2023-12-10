# app.py
# Seleciona as bibliotcas
from flask_openapi3 import OpenAPI, Info, Tag
from flask import Flask, request, redirect, jsonify
from sqlalchemy.exc import IntegrityError
from model import Session, Cadastro, Endereco
from schemas import (
    LoginSchema,
    CadastroSchema,
    ErrorSchema,
    EnderecoSchema,
    AtualizarCadastroSchema,
    EnderecoDeleteSchema,
    EnderecoSearchParams,
    EnderecoSchemaCompleto
)
from flask_cors import CORS
from logger import logger

info = Info(title="API - Next Logistics WMS ", version="1.0.0")
app = OpenAPI(__name__, info=info)

# Configuração do CORS para que um domínio diferente possa acessar a aplicação
CORS(app)

# Cria as tags para o Swagger
cadastro_tag = Tag(name="Cadastro", description="Operações relacionadas ao cadastro de um usúario")
endereco_tag = Tag(name="Endereco", description="Operações relacionadas ao endereço de um material em um armazém")

"""
╔═══════════════════════════════════════════════════════════════════════════════════════════════════════════════╗                                                            
║                                                                                                               ║  
 ■  As três rotas abaixo são relativas ao login, cadastro e mudança de senha do usuário 👤 (Tabela cadastro)   ■
║                                                                                                               ║ 
╚═══════════════════════════════════════════════════════════════════════════════════════════════════════════════╝  
"""

# Rota para verificar se o usúario está cadastrado
@app.post('/login', tags=[cadastro_tag],
          responses={"200": ErrorSchema, "401": ErrorSchema, "400": ErrorSchema})
def login(form: LoginSchema):
    """Verifica o login e retorna um JSON e o status indicando o sucesso ou falha da operação"""
    try:
        # Query buscando pelo nome e senha
        session = Session()
        cadastro = session.query(Cadastro).filter_by(nome=form.nome, senha=form.senha).first()
        # Se existe um usuario
        if cadastro:
            # Usuário autenticado
            return jsonify({"message": "Login bem-sucedido. Seja bem vindo"}), 200
        # Não existe
        else:
            # Nome de usuário ou senha incorretos
            return {"message": "Nome de usuário ou senha incorretos. Tente novamente ou cadastre um usuário"}, 401
    #Outros casos
    except Exception as e:
        return {"message": "Erro durante o login :/"}, 400

# Rota para cadastrar um usuário
@app.post('/cadastro',  tags=[cadastro_tag],
          responses={"200": CadastroSchema, "409": ErrorSchema, "400": ErrorSchema})
def add_cadastro(form: CadastroSchema):   
    """Adiciona um novo Cadastro à base de dados. Não pode ser inserido um usuário com mesmo nome e senha mais de uma vez"""
    try:
        session = Session()
        # Verificar se já existe um usuário com o mesmo nome e senha
        if session.query(Cadastro).filter_by(nome=form.nome).first():
            error_msg = "Nome de usuário já cadastrado. Digite um usuário ou senha diferente"
            return {"message": error_msg}, 409
        # Adicionar o novo usuário
        cadastro = Cadastro(nome=form.nome, senha=form.senha)
        session.add(cadastro)
        # Faz o commit adicionando um novo usuário
        session.commit()
        return {"id": cadastro.id, "nome": cadastro.nome, "senha": cadastro.senha}, 200
    # Outro erro
    except Exception as e:
        error_msg = "Não foi possível salvar novo Cadastro :/"
        return {"message": error_msg}, 400
    
# Rota para atuaizar um cadastro é necessário fornecer o nome e senha corretos para cadastrar    
@app.post('/atualizar_cadastro', tags=[cadastro_tag],
          responses={"200": CadastroSchema, "400": ErrorSchema})
def atualizar_cadastro(form: AtualizarCadastroSchema):
    """Atualiza a senha de um cadastro específico. Necessário que o mesmo nome e senha já estejam cadastrados"""
    nome = form.nome
    senha = form.senha
    senha_nova = form.senha_nova
    # Filtra o no tabela cadastro o nome e a senha inseridos
    try:
        session = Session()
        cadastro = session.query(Cadastro).filter_by(nome=nome, senha=senha).first()

        if cadastro:
            cadastro.senha = senha_nova
            session.commit()
            return {"id": cadastro.id, "nome": cadastro.nome, "senha": cadastro.senha}, 200
        else:
            error_msg = "Nome de usuário ou senha incorretos :/"
            return {"message": error_msg}, 400
    # Outro erro
    except Exception as e:
        error_msg = "Não foi possível atualizar a senha :/"
        return {"message": error_msg}, 400    
"""
╔═══════════════════════════════════════════════════════════════════════════════════════════════════════════════╗                                                            
║                                                                                                               ║  
 ■    As três rotas abaixo são relativas ao endereçamento, novo, exclusão  e busca 🏢 (Tabela enderço)         ■  
║                                                                                                               ║ 
╚═══════════════════════════════════════════════════════════════════════════════════════════════════════════════╝  
"""

# Rota para adicionar um novo produto a uma posição do estoque
@app.post('/endereco', tags=[endereco_tag],
          responses={"200": EnderecoSchema, "400": ErrorSchema})
def add_endereco(form: EnderecoSchema):
    """Adiciona um novo item a uma posição específica do estoque. Não pode ter outro item na mesma posição e rua"""
    rua = form.rua
    posicao = form.posicao
    try:
        session = Session()
        # Verificar se já existe um item na mesma posição e rua
        existing_item = session.query(Endereco).filter_by(rua=rua, posicao=posicao).first()
        if existing_item:
            # Se existir, cria uma mensagem de erro contendo os detalhes e depois exibe para o usuário
            error_msg = f"Já existe um item na posição {posicao} da rua {rua}"
            return {"message": error_msg}, 400
        # Adicionar um novo item se não existir um na mesma posição e rua
        new_endereco = Endereco(
            material=form.material,
            quantidade=form.quantidade,
            sku=form.sku,
            rua=rua,
            posicao=posicao,
            nome=form.nome
        )
        session.add(new_endereco)
        session.commit()
        
        return {"id": new_endereco.id, "material": new_endereco.material, "posicao": new_endereco.posicao, "quantidade": new_endereco.quantidade, "rua": new_endereco.rua, "sku": new_endereco.sku, "nome": new_endereco.nome}, 200

    except Exception as e:
        error_msg = "Não foi possível adicionar o item no Endereco :/"
        return {"message": error_msg}, 400

# Rota para excluir um item do Endereco
@app.delete('/endereco_apagar', tags=[endereco_tag],
          responses={"200": EnderecoSchema, "400": ErrorSchema})
            
def delete_endereco(form: EnderecoDeleteSchema):
    """Exclui um item do de uma posição por ID inserido pelo usuário"""
    logger.info("Chamaram o Delete")
    try:
        session = Session()
        endereco_id = form.endereco_id
        endereco = session.query(Endereco).filter_by(id=endereco_id).first()

        if endereco:
            session.delete(endereco)
            session.commit()
            return {"message": "Item excluído com sucesso!"}, 200
        else:
            error_msg = "Endereço não encontrado :/"
            return {"message": error_msg}, 400

    except Exception as e:
        error_msg = "Não foi possível excluir o item do Endereco :/"
        return {"message": error_msg}, 400

# Rota para trazer todos os itens com base na rua ou posicao
@app.get('/endereco_buscar', tags=[endereco_tag], responses={"200": EnderecoSchemaCompleto, "404": ErrorSchema})
def get_produto(query: EnderecoSearchParams):
    """Faz a busca por um Produto a partir da rua ou da posicao"""
    # criando conexão com a base
    session = Session()
    posicao = query.posicao
    rua = query.rua
    logger.debug(f"Coletando dados sobre produto #{posicao} e material #{rua}")
   
    # fazendo a busca
    produtos = []
    if posicao and rua:
        produtos = session.query(Endereco).filter(Endereco.posicao == posicao, Endereco.rua == rua).all()
    elif posicao:
        produtos = session.query(Endereco).filter(Endereco.posicao == posicao).all()
    elif rua:
        produtos = session.query(Endereco).filter(Endereco.rua == rua).all()
    else:
        return {"message": "Nenhum parâmetro fornecido"}

    if not produtos:
        # se o produto não foi encontrado
        error_msg = "Produto não encontrado na base :/"
        logger.warning(f"Erro ao buscar produto, {error_msg}")
        return {"message": "Deu errado"}, 404
    else:
        produtos_dict = [{"id": produto.id, "material": produto.material, "quantidade": produto.quantidade, "sku": produto.sku, "rua": produto.rua, "posicao": produto.posicao, "nome": produto.nome} for produto in produtos]
        logger.debug(f"Produtos encontrados: {len(produtos_dict)}")
        return {"message": "Deu certo", "produtos": produtos_dict}, 200


@app.route('/')
def redirect_to_swagger():
    return redirect('/openapi')
