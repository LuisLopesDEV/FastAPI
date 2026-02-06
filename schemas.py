from pydantic import BaseModel
from typing import Optional, List


class UsuarioSchemas(BaseModel):
    """
    Schema para criação de usuários.
    """
    nome: str
    email: str
    senha: str
    ativo: Optional[bool]
    admin: Optional[bool] = False

    class Config:
        from_attributes = True


class PedidoSchemas(BaseModel):
    """
    Schema para criação de pedidos.
    """
    usuario: int

    class Config:
        from_attributes = True


class LoginSchema(BaseModel):
    """
    Schema para autenticação de usuários.
    """
    email: str
    senha: str

    class Config:
        from_attributes = True


class ItemPedidoSchema(BaseModel):
    """
    Schema para criação de itens de pedido.
    """
    quantidade: int
    sabor: str
    tamanho: str
    preco_unitario: float

    class Config:
        from_attributes = True


class ResponsePedidoSchema(BaseModel):
    """
    Schema de resposta para pedidos.
    """
    id: int
    status: str
    preco: float
    itens: List[ItemPedidoSchema]

    class Config:
        from_attributes = True
