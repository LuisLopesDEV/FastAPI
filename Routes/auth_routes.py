from fastapi import APIRouter, Depends, HTTPException
from DataBase.models import User
from Routes.dependencies import pegar_session
from schemas import UsuarioSchemas, LoginSchema
from sqlalchemy.orm import Session
import bcrypt
auth_router = APIRouter(prefix="/auth", tags=['Auth'])


def criar_token(email):
    token = f'fnakojlhdwlkanfa{email}'
    return token
@auth_router.get('/')
async def home():
    return {'message': 'Path Auth'}

@auth_router.post('/signup')
async def signup(usuario_schema: UsuarioSchemas, session: Session = Depends(pegar_session)):
    senha_bytes = usuario_schema.senha.encode('utf-8')
    hash = bcrypt.hashpw(senha_bytes, bcrypt.gensalt())
    hash_senha = hash.decode('utf-8')

    usuario = session.query(User).filter(User.email == usuario_schema.email).first()

    if usuario:
        raise HTTPException(status_code=400, detail="Email do usuário já cadastrada")
    else:
        novo_usuario = User(usuario_schema.nome, usuario_schema.email, hash_senha, usuario_schema.ativo, usuario_schema.admin)
        session.add(novo_usuario)
        session.commit()
        return {'mensagem': f'Usuário criado com sucesso! Email: {usuario_schema.email}'}

@auth_router.post('/login')
async def login(login_schema: LoginSchema, session: Session = Depends(pegar_session)):

    usuario = session.query(User).filter(User.email == login_schema.email).first()

    if not usuario:
        raise HTTPException(status_code=400, detail='Email ou senha incorreto')
    else:
        access_token = criar_token(usuario.email)
        return {"access_token": access_token, "token_type": "bearer"}
