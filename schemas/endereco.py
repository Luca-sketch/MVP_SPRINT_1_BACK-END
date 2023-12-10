from typing import Optional
from pydantic import BaseModel
from datetime import datetime
class EnderecoSchema(BaseModel):
    material: str
    quantidade: int
    sku: str
    rua: str
    posicao: str
    nome: str
    data_insercao: Optional[datetime] = None  
    
class EnderecoSchemaCompleto(BaseModel):
    id: int
    material: str
    quantidade: int
    sku: str
    rua: str
    posicao: str
    nome: str
    data_insercao: Optional[datetime] = None  
    
from pydantic import BaseModel

class EnderecoDeleteSchema(BaseModel):
    endereco_id: int
    
class EnderecoSearchParams(BaseModel):
      posicao: Optional[str] = None
      rua: Optional[str] = None