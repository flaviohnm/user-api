from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel, EmailStr, validator
from datetime import datetime, timedelta
from jose import JWTError, jwt
from typing import Optional
from dotenv import load_dotenv
import os

load_dotenv()

# Configurações
SECRET_KEY = os.getenv('SECRET_KEY')
ALGORITHM = os.getenv('ALGORITHM')
USERNAME = os.getenv('USERNAME')
PASSWORD = os.getenv('PASSWORD')
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Modelo de dados para o usuário
class User(BaseModel):
    nome: str
    email: EmailStr
    cpf: str
    data_nascimento: str

    @validator("cpf")
    def validate_cpf(cls, v):
        if not v.replace(".", "").replace("-", "").isdigit() or len(v) != 14:
            raise ValueError("CPF inválido. Formato esperado: XXX.XXX.XXX-XX")
        return v

    @validator("data_nascimento")
    def validate_data_nascimento(cls, v):
        try:
            datetime.strptime(v, "%Y-%m-%d")
        except ValueError:
            raise ValueError(
                "Data de nascimento inválida. Formato esperado: YYYY-MM-DD"
            )
        return v


# Modelo de dados para o token
class Token(BaseModel):
    access_token: str
    token_type: str


# Banco de dados em memória
fake_users_db = []
fake_users_auth_db = {"userTest": {"username": "userTest", "password": PASSWORD}}

# Função para criar token JWT
def create_jwt_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


# Função para autenticar o usuário
def authenticate_user(username: str, password: str):
    user = fake_users_auth_db.get(username)
    if not user:
        return False
    if user["password"] != password:
        return False
    return user


# Função para validar o token JWT
async def get_current_user(
    token: str = Depends(OAuth2PasswordBearer(tokenUrl="token")),
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Não foi possível validar as credenciais",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = fake_users_auth_db.get(username)
    if user is None:
        raise credentials_exception
    return user


# Inicialização do FastAPI
app = FastAPI()


# Endpoint para gerar token JWT
@app.post("/token/", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuário ou senha incorretos",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_jwt_token(
        data={"sub": user["username"]}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


# Endpoint para cadastrar usuários (protegido por autenticação)
@app.post("/usuarios/", status_code=status.HTTP_201_CREATED)
async def criar_usuario(user: User, current_user: dict = Depends(get_current_user)):
    user_dict = user.dict()
    # Simula um ID gerado pelo banco de dados
    user_dict["id"] = len(fake_users_db) + 1
    fake_users_db.append(user_dict)
    return user_dict


# Endpoint para listar todos os usuários (apenas para teste)
@app.get("/usuarios/")
async def listar_usuarios():
    return fake_users_db
