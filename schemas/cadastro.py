from pydantic import BaseModel

# Schema para realizar o login
class LoginSchema(BaseModel):
    nome: str
    senha: str

# Schema parar cadastrar um novo usuário
class CadastroSchema(BaseModel):
    nome: str
    senha: str

# Schema de atualizar um castro
class AtualizarCadastroSchema(BaseModel):
    nome: str
    senha: str
    senha_nova: str