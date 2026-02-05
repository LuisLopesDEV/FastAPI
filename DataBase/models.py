from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey, Boolean, Float
from sqlalchemy.orm import declarative_base
from sqlalchemy_utils.types import ChoiceType
import bcrypt

db = create_engine("mysql+pymysql://root:@localhost:3306/meubanco")

Base = declarative_base()

class User(Base):
    __tablename__ = "users"


    id = Column("id", Integer, primary_key=True, autoincrement=True, nullable=False)
    name = Column("name", String(50), nullable=False)
    email = Column("email", String(50), unique=True, nullable=False)
    senha = Column("senha", String(500), nullable=False)
    ativo = Column("ativo", Boolean, nullable=False)
    admin = Column("admin", Boolean, default=False)


    def __init__(self, name, email, senha, ativo=True, admin=False):
        self.name = name
        self.email = email
        self.senha = senha
        self.ativo = ativo
        self.admin = admin

class Pedido(Base):
    __tablename__ = "pedidos"

    STATUS_PEDIDOS = (
        ("PENDENTE", "PENDENTE"),
        ("CANCELADO", "CANCELADO"),
        ("FINALIZADO", "FINALIZADO")
    )

    id = Column("id", Integer, primary_key=True, autoincrement=True, nullable=False)
    status = Column("status", String(50), nullable=False) # Pendente, Cancelado, Finalizado
    usuario = Column("usuario", ForeignKey('users.id'), nullable=False)
    preco = Column("preco", Float, nullable=False)
    #itens =

    def __init__(self,usuario, status="PENDENTE", preco=0):
        self.status = status
        self.usuario = usuario
        self.preco = preco

    def calcular_preco(self):
        self.preco = 10

class ItemPedido(Base):
    __tablename__ = "itens_pedidos"

    id = Column("id", Integer, primary_key=True, autoincrement=True)
    quantidade = Column("quantidade", Integer, nullable=False)
    sabor = Column("sabor", String(50), nullable=False)
    tamanho = Column("tamanho", String(50), nullable=False)
    preco_unitario = Column("preco_unitario", Float, nullable=False)
    pedido = Column("pedido", ForeignKey('pedidos.id'), nullable=False)

    def __init__ (self, sabor, pedido, tamanho, quantidade=1, preco_unitario=0):
        self.sabor = sabor
        self.pedido = pedido
        self.tamanho = tamanho
        self.quantidade = quantidade
        self.preco_unitario = preco_unitario
