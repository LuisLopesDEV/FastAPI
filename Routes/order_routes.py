from fastapi import APIRouter, Depends, HTTPException
from Routes.dependencies import pegar_session, verificar_token
from schemas import PedidoSchemas, ItemPedidoSchema, ResponsePedidoSchema
from sqlalchemy.orm import Session
from DataBase.models import Pedido, User, ItemPedido
from typing import List
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

    if not usuario.admin and usuario.id != pedido.usuario:
        raise HTTPException(
            status_code=403, detail='Você não tem autorização para cancelar este pedido')

    pedido.status = 'CANCELADO'
    session.commit()
    return {
        'mensagem': f'Pedido {pedido.id} cancelado com sucesso!',
        'pedido': pedido
    }

@order_router.get('/listar')
async def listar_pedidos(usuario: User = Depends(verificar_token), session: Session = Depends(pegar_session)):
    if not usuario.admin:
        raise HTTPException(
            status_code=403, detail='Você não tem autorização para fazer essa operação')
    else:
        pedidos = session.query(Pedido).all()
        return {'pedidos': pedidos}

@order_router.post('/pedido/adcionar/{id_pedido}')
async def adcionar_item(id_pedido: int,
                        item_pedido_schema: ItemPedidoSchema,
                        usuario: User = Depends(verificar_token),
                        session: Session = Depends(pegar_session)):

    pedido = session.query(Pedido).filter(Pedido.id==id_pedido).first()

    if not pedido:
        raise HTTPException(status_code=400, detail='Pedido não existe')
    if not usuario.admin and usuario.id != pedido.usuario:
        raise HTTPException(status_code=403, detail='Você não tem autorização para fazer essa operação')

    item_pedido = ItemPedido(
        sabor=item_pedido_schema.sabor,
        pedido=id_pedido,
        tamanho=item_pedido_schema.tamanho,
        quantidade=item_pedido_schema.quantidade,
        preco_unitario=item_pedido_schema.preco_unitario
    )

    session.add(item_pedido)
    pedido.calcular_preco()
    session.commit()
    return {
        'mensagem': 'Item criado com sucesso!',
        'item_id': item_pedido.id,
        'preco_pedido': pedido.preco
    }

@order_router.post('/pedido/remover/{id_item_pedido}')
async def remover_item(id_item_pedido: int,
                        usuario: User = Depends(verificar_token),
                        session: Session = Depends(pegar_session)):

    item_pedido = session.query(ItemPedido).filter(ItemPedido.id==id_item_pedido).first()
    pedido = session.query(Pedido).filter(Pedido.id==item_pedido.pedido).first()
    if not item_pedido:
        raise HTTPException(status_code=400, detail='Pedido não existe')
    if not usuario.admin and usuario.id != pedido.usuario:
        raise HTTPException(status_code=403, detail='Você não tem autorização para fazer essa operação')

    session.delete(item_pedido)
    pedido.calcular_preco()
    session.commit()
    return {
        'mensagem': 'Item removido com sucesso!',
        'quant_itens_pedido': len(pedido.itens),
        'pedido': pedido
    }

@order_router.post('/pedidos/finalizar/{id_pedido}')
async def finalizar_pedido(id_pedido: int, session: Session = Depends(pegar_session), usuario: User = Depends(verificar_token)):
    pedido = session.query(Pedido).filter(Pedido.id==id_pedido).first()
    if not pedido:
        raise HTTPException(status_code=400, detail='Pedido não encontrado')

    if not usuario.admin and usuario.id != pedido.usuario:
        raise HTTPException(
            status_code=403, detail='Você não tem autorização para cancelar este pedido')

    pedido.status = 'FINALIZADO'
    session.commit()
    return {
        'mensagem': f'Pedido {pedido.id} finalizado com sucesso!',
        'pedido': pedido
    }

@order_router.get('/pedido/{id_pedido}')
async def ver_pedido(id_pedido: int, usuario: User = Depends(verificar_token), session: Session = Depends(pegar_session)):
    pedido = session.query(Pedido).filter(Pedido.id==id_pedido).first()
    if not pedido:
        raise HTTPException(status_code=400, detail='Pedido não encontrado')
    if not usuario.admin and usuario.id != pedido.usuario:
        raise HTTPException(
            status_code=403, detail='Você não tem autorização para cancelar este pedido')
    return {
        'quantidade_itens': len(pedido.itens),
        'pedido': pedido
    }

@order_router.get('/listar/pedidos-usuario', response_model=List[ResponsePedidoSchema])
async def listar_pedidos(usuario: User = Depends(verificar_token), session: Session = Depends(pegar_session)):
    pedidos = session.query(Pedido).filter(Pedido.usuario==usuario.id).all()
    return pedidos
