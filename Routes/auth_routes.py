from fastapi import APIRouter, Depends, HTTPException
from DataBase.models import User
from Routes.dependencies import pegar_session, verificar_token
from main import SECRET_KEY, ALGORITHM, ACCES_TOKEN_EXPIRES_MINUTES
from schemas import UsuarioSchemas, LoginSchema
from sqlalchemy.orm import Session
import bcrypt
from jose import jwt,JWTError
from datetime import datetime, timedelta, timezone
from fastapi.security import OAuth2PasswordRequestForm
auth_router = APIRouter(prefix="/auth", tags=['Auth'])

def criar_token(id_usuario, duracao_token=timedelta(minutes=ACCES_TOKEN_EXPIRES_MINUTES)):
    data_expiracao = datetime.now(timezone.utc) + duracao_token
    dic_info = {'sub': str(id_usuario), 'exp': data_expiracao}
    jwt_codificado = jwt.encode(dic_info, SECRET_KEY, ALGORITHM)
    return jwt_codificado

def autenticar_usuario(email, senha, session):
    usuario = session.query(User).filter(User.email == email).first()
    senha_bytes = senha.encode('utf-8')

    if not usuario:
        return False
    if not bcrypt.checkpw(senha_bytes, usuario.senha.encode('utf-8')):
        return False
    return usuario



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
    usuario = autenticar_usuario(login_schema.email, login_schema.senha, session)
    if not usuario:
        raise HTTPException(status_code=400, detail="Email ou senha incorreto")
    else:
        access_token = criar_token(usuario.id)
        refresh_token = criar_token(usuario.id, duracao_token=timedelta(days=7))
        return {
                'access_token': access_token,
                'refresh_token': refresh_token,
                'token_type': 'bearer'
        }

@auth_router.post('/login-form')
async def login_form(dados_formulario: OAuth2PasswordRequestForm = Depends(), session: Session = Depends(pegar_session)):
    usuario = autenticar_usuario(dados_formulario.username, dados_formulario.password, session)
    if not usuario:
        raise HTTPException(status_code=400, detail="Email ou senha incorreto")
    else:
        access_token = criar_token(usuario.id)
        return {
                'access_token': access_token,
                'token_type': 'bearer'
        }

@auth_router.get('/refresh')
async def use_refresh_token(usuario: User= Depends(verificar_token)):
    access_token = criar_token(usuario.id)
    return {
        'access_token': access_token,
        'token_type': 'Bearer'
    }

