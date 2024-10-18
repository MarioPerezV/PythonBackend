# ENCRIPTACION DEL BACKEND
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt, JWTError
from passlib.context import CryptContext
from datetime import datetime, timedelta

# Encryptar: **ojo** las constantes las hace en mayusculas?
ALGORITHM="HS256"
ACCESS_TOKEN_DURATION = 1
# to get a string like this run en la misma terminal:
# openssl rand -hex 32      -- es un numero aleatorio hexadecimal de 32bits
SECRET="1a82814c2333b3808f8e32ae9c58db2e24c120ca2bff57568210b3db97a59e29" # secret = también puede ser lo que sea, un conjunto de caracteres aleatorios o estandarizados
crypt=CryptContext(schemes=["bcrypt"])

# Casi Todos LOS ERRORES FUERON POR NO COHERENCIA ENTRE THUNDER CLIENT y LA CARPETA routers. Eso...
router = APIRouter()
oauth2=OAuth2PasswordBearer(tokenUrl="login") # Estandar que dice como se debe trabajar en autenticacion en un backend

class User(BaseModel): # Click para la documentacion de la herencia BaseModel
  username: str
  name: str
  email: str
  disable: bool
  
class UserDB(User):
  password: str
  
users_db={
  "Mario": {
    "username": "Mario",
    "name": "Mario Perez",
    "email": "stmario@gmail.com",
    "disable": False,
    "password": "$2a$12$Onw08vylarmdtmW8tMxlpOsN.SZIBrnoZi.QI9pruNdhZ/TnFOxjy"}, # 1234
  "Lolo": {
    "username": "Lolo",
    "name": "Lolo Perez",
    "email": "lolo@gmail.com",
    "disable": True,
    "password": "$2a$12$brgjLSDuvAfuBbPPTv.EAOC3.OBHWqcxmcIQpFVslOiE9cQVZSYnu"} # 1235
}

def search_user_db(username:str):
  if username in users_db:
    return UserDB(**users_db[username])
  
def search_user(username:str):
  if username in users_db:
    return User(**users_db[username])

async def auth_user(token:str= Depends(oauth2)):
  exception=HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Credenciales de autenticacion incorrectas o inválidas", headers={"WWW-Authenticate":"Bearer"})
  try:
    username=jwt.decode(token, SECRET, algorithms=[ALGORITHM]).get("sub")
    if username is None:
      raise exception
  except JWTError:
    raise exception
  
  return search_user(username)  

async def current_user(user:User= Depends(auth_user)):  
  if user.disable:
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Credenciales de autenticacion incorrectas o inválidas", headers={"WWW-Authenticate":"Bearer"}) # protocolo extricto. Una falta de ortografía y todo mal
  if user.disable:
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Usuario Inactivo")
  return user

# Operacion de autenticacion usuario y contraseña
@router.post("/login")
async def login(form: OAuth2PasswordRequestForm = Depends()):
  user_db = users_db.get(form.username)
  if not user_db:
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="El usuario es incorrecto")
  
  user=search_user_db(form.username)
    
  user = search_user_db(form.username)
  if not crypt.verify(form.password, user.password): # Se entregan las contraseñas a las contraseñas encriptadas de la base de datos
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="La contraseña es incorrecta")
  
  access_token={"sub":user.username, 
                "exp":datetime.utcnow()+timedelta(minutes=ACCESS_TOKEN_DURATION)}
    
  return {"access_token":jwt.encode(access_token, SECRET, algorithm=ALGORITHM),"token_type":"bearer"}

@router.get("/users/me")
async def me(user:User = Depends(current_user)):
  return user