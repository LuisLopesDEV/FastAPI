from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey, Boolean, Float
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy_utils.types import ChoiceType
import bcrypt

db = create_engine("mysql+pymysql://root:@localhost:3306/meubanco")

Base = declarative_base()


class User(Base):
    """
    Model que representa um usuário do sistema.

    Attributes:
        id (int): Identificador único do usuário.
        name (str): Nome do usuário.
        email (str): Email do usuário (único).
        senha (str): Senha do usuário (hash).
        ativo (bool): Indica se o usuário está ativo.
        admin (bool): Indica se o usuário possui permissões administrativas.
    """

    __tablename__ = "users"

    id = Column("id", Integer, primary_key=True, autoincrement=True, nullable=False)
    name = Column("name", String(50), nullable=False)
    email = Column("email", String(50), unique=True, nullable=False)
    senha = Column("senha", String(500), nullable=False)
    ativo = Column("ativo", Boolean, nullable=False)
    admin = Column("admin", Boolean, default=False)

    def __init__(self, name, email, senha, ativo=True, admin=False):
        """
        Inicializa um novo usuário.

        Args:
            name (str): Nome do usuário.
            email (str): Email do usuário.
            senha (str): Senha do usuário.
            ativo (bool, optional): Define se o usuário está ativo.
            admin (bool, optional): Define se o usuário é administrador.
        """
        self.name = name
        self.email = email
        self.senha = senha
        self.ativo = ativo
        self.admin = admin


class Pedido(Base):
    """
    Model que representa um pedido realizado por um usuário.

    Attributes:
        id (int): Identificador do pedido.
        status (str): Status do pedido (PENDENTE, CANCELADO, FINALIZADO).
        usuario (int): ID do usuário dono do pedido.
        preco (float): Valor total do pedido.
        itens (list): Lista de itens associados ao pedido.
    """

    __tablename__ = "pedidos"

    STATUS_PEDIDOS = (
        ("PENDENTE", "PENDENTE"),
        ("CANCELADO", "CANCELADO"),
        ("FINALIZADO", "FINALIZADO")
    )

    id = Column("id", Integer, primary_key=True, autoincrement=True, nullable=False)
    status = Column("status", String(50), nullable=False)
    usuario = Column("usuario", ForeignKey('users.id'), nullable=False)
    preco = Column("preco", Float, nullable=False)
    itens = relationship("ItemPedido", cascade="all, delete")

    def __init__(self, usuario, status="PENDENTE", preco=0):
        """
        Inicializa um novo pedido.

        Args:
            usuario (int): ID do usuário.
            status (str, optional): Status inicial do pedido.
            preco (float, optional): Preço inicial.
        """
        self.status = status
        self.usuario = usuario
        self.preco = preco

    def calcular_preco(self):
        """
        Calcula e atualiza o preço total do pedido
        com base nos itens associados.
        """
        self.preco = sum(item.preco_unitario * item.quantidade for item in self.itens)


class ItemPedido(Base):
    """
    Model que representa um item pertencente a um pedido.

    Attributes:
        id (int): Identificador do item.
        quantidade (int): Quantidade do item.
        sabor (str): Sabor do item.
        tamanho (str): Tamanho do item.
        preco_unitario (float): Preço unitário.
        pedido (int): ID do pedido associado.
    """

    __tablename__ = "itens_pedidos"

    id = Column("id", Integer, primary_key=True, autoincrement=True)
    quantidade = Column("quantidade", Integer, nullable=False)
    sabor = Column("sabor", String(50), nullable=False)
    tamanho = Column("tamanho", String(50), nullable=False)
    preco_unitario = Column("preco_unitario", Float, nullable=False)
    pedido = Column("pedido", ForeignKey('pedidos.id'), nullable=False)

    def __init__(self, sabor, pedido, tamanho, quantidade, preco_unitario):
        """
        Inicializa um novo item de pedido.

        Args:
            sabor (str): Sabor do item.
            pedido (int): ID do pedido.
            tamanho (str): Tamanho do item.
            quantidade (int): Quantidade.
            preco_unitario (float): Preço unitário.
        """
        self.sabor = sabor
        self.pedido = pedido
        self.tamanho = tamanho
        self.quantidade = quantidade
        self.preco_unitario = preco_unitario
