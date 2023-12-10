from sqlalchemy import Column, String, Integer, DateTime
from datetime import datetime
from model.base import Base

class Endereco(Base):
    __tablename__ = 'endereco'

    id = Column(Integer, primary_key=True, autoincrement=True)
    material = Column(String(255))
    quantidade = Column(Integer)
    sku = Column(String(255))
    rua = Column(String(255))
    posicao = Column(String(255))
    nome = Column(String(255))
    data_insercao = Column(DateTime, default=datetime.now())