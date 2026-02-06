from fastapi import APIRouter, Depends, HTTPException
from DataBase.models import User
from Routes.dependencies import pegar_session, verificar_token
from main import SECRET_KEY, ALGORITHM, ACCES_TOKEN_EXPIRES_MINUTES
from schemas import UsuarioSchemas, LoginSchema
from sqlalchemy.orm import Session
import bcrypt
from jose import jwt
from datetime import datetime, timedelta, timezone
from fastapi.security import OAuth2PasswordRequestForm

auth_router = APIRouter(prefix="/auth", tags=['Auth'])


def criar_token(id_usuario, duracao_token=timedelta(minutes=ACCES_TOKEN_EXPIRES_MINUTES)):
    """
    Cria um token JWT para autenticação.

    Args:
        id_usuario (int): ID do usuário.
        duracao_token (timedelta): Tempo de expiração do token.

    Returns:
        str: Token JWT codificado.
    """
    data_expiracao = datetime.now(timezone.utc) + duracao_token
    dic_info = {'sub': str(id_usuario), 'exp': data_expiracao}
    return jwt.encode(dic_info, SECRET_KEY, ALGORITHM)


def autenticar_usuario(email, senha, session):
    """
    Autentica um usuário verificando email e senha.

    Args:
        email (str): Email do usuário.
        senha (str): Senha informada.
        session (Session): Sessão do banco.

    Returns:
        User | bool: Usuário autenticado ou False.
    """
    usuario = session.query(User).filter(User.email == email).first()
    if not usuario:
        return False

    if not bcrypt.checkpw(senha.encode('utf-8'), usuario.senha.encode('utf-8')):
        return False

    return usuario
