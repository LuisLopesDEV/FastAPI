from fastapi import APIRouter, Depends, HTTPException
from Routes.dependencies import pegar_session
from schemas import PedidoSchemas
from sqlalchemy.orm import Session
from DataBase.models import Pedido
order_router = APIRouter(prefix="/order", tags=['Order'])

@order_router.get("/")
async def pedidos():
    return {"message": "Path order"}

@order_router.post('/pedidos')
async def criar_pedidos(pedido_schema: PedidoSchemas, session: Session = Depends(pegar_session)):
    novo_pedido=Pedido(pedido_schema.usuario)
    session.add(novo_pedido)
    session.commit()
    return {"message": f"Pedido criado com sucesso! ID do pedido: {novo_pedido.id}"}
