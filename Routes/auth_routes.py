from fastapi import APIRouter
from DataBase.models import User, db
from sqlalchemy.orm import sessionmaker
import bcrypt
auth_router = APIRouter(prefix="/auth", tags=['Auth'])

@auth_router.get('/')
async def home():
    return {'message': 'Path Auth'}

@auth_router.post('/signup')
async def signup(nome: str, email:str, senha: str, session):
    senha_bytes = senha.encode('utf-8')
    hash = bcrypt.hashpw(senha_bytes, bcrypt.gensalt())
    hash_senha = hash.decode('utf-8')
    sessions = sessionmaker(bind=db)
    session = sessions()
    usuario = session.query(User).filter(User.email == email).first()

    if usuario:
        return {'mensagem': 'Usuário já existe'}
    else:
        novo_usuario = User(nome, email, hash_senha)
        session.add(novo_usuario)
        session.commit()
        return {'mensagem': 'Usuário criado com sucesso!'}
