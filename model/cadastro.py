from sqlalchemy import Column, String, Integer
from model.base import Base

class Cadastro(Base):
    __tablename__ = 'cadastro'

    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(255), nullable=False)
    senha = Column(String(255), nullable=False)