from fastapi import APIRouter, Depends, HTTPException
from Routes.dependencies import pegar_session, verificar_token
from schemas import PedidoSchemas
from sqlalchemy.orm import Session
from DataBase.models import Pedido, User
order_router = APIRouter(prefix="/order", tags=['Order'], dependencies=[Depends(verificar_token)])

@order_router.get("/")
async def pedidos():
    return {"message": "Path order"}

@order_router.post('/pedidos')
async def criar_pedidos(pedido_schema: PedidoSchemas, session: Session = Depends(pegar_session)):
    novo_pedido=Pedido(pedido_schema.usuario)
    session.add(novo_pedido)
    session.commit()
    return {"message": f"Pedido criado com sucesso! ID do pedido: {novo_pedido.id}"}

@order_router.post('/pedidos/cancelar/{id_pedido}')
async def cancelar_pedido(id_pedido: int, session: Session = Depends(pegar_session), usuario: User = Depends(verificar_token)):
    pedido = session.query(Pedido).filter(Pedido.id==id_pedido).first()
    if not pedido:
        raise HTTPException(status_code=400, detail='Pedido não encontrado')
    print("usuario.id =", usuario.id)
    print("pedido.usuario =", pedido.usuario)
    print("usuario.admin =", usuario.admin)
    if not usuario.admin and usuario.id != pedido.usuario:
        raise HTTPException(
            status_code=403,
            detail='Você não tem autorização para cancelar este pedido'
        )

    pedido.status = 'CANCELADO'
    session.commit()
    return {
        'mensagem': f'Pedido {id_pedido} cancelado com sucesso!',
        'pedido': pedido
    }
