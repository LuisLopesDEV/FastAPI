from fastapi import Depends, HTTPException
from DataBase.models import db, User
from sqlalchemy.orm import sessionmaker, Session
from jose import jwt, JWTError
from main import SECRET_KEY, ALGORITHM, oauth2_schema


def pegar_session():
    """
    Cria e fornece uma sessão do banco de dados.

    Yields:
        Session: Sessão ativa do SQLAlchemy.
    """
    try:
        SessionLocal = sessionmaker(bind=db)
        session = SessionLocal()
        yield session
    finally:
        session.close()


def verificar_token(token: str = Depends(oauth2_schema), session: Session = Depends(pegar_session)):
    """
    Valida o token JWT e retorna o usuário autenticado.

    Args:
        token (str): Token JWT.
        session (Session): Sessão do banco de dados.

    Returns:
        User: Usuário autenticado.

    Raises:
        HTTPException: Se o token for inválido ou usuário não existir.
    """
    try:
        dic_info = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id_usuario = int(dic_info.get("sub"))
    except JWTError:
        raise HTTPException(status_code=401, detail='Acesso Negado')

    usuario = session.query(User).filter(User.id == id_usuario).first()
    if not usuario:
        raise HTTPException(status_code=401, detail='Acesso Inválido')

    return usuario
