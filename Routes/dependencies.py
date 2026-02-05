from http.client import HTTPException

from fastapi import Depends, HTTPException
from DataBase.models import db
from sqlalchemy.orm import sessionmaker, Session
from DataBase.models import User
from jose import jwt, JWTError
from main import SECRET_KEY, ALGORITHM, oauth2_schema


def pegar_session():
    try:
        Session = sessionmaker(bind=db)
        session = Session()
        yield session
    finally:
        session.close()

def verificar_token(token: str =  Depends(oauth2_schema), session: Session = Depends(pegar_session)):
    try:
        dic_info = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id_usuario = int(dic_info.get("sub"))
    except JWTError:
        raise HTTPException(status_code=401, detail='Acesso Negado')

    usuario = session.query(User).filter(User.id == id_usuario).first()
    if not usuario:
        raise HTTPException(status_code=401, detail='Acesso Inválido')

    return usuario
