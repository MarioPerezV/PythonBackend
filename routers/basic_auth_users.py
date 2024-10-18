from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

# ¿HACEMOS UN ROUTER? router = APIRouter(prefix="/products",tags=["products"], responses={404: {"mensaje":"No encontrado"}})
router = APIRouter()
# Casi todos LOS ERRORES FUERON POR NO COHERENCIA ENTRE THUNDER CLIENT y LA CARPETA routers. Eso...
# app=FastAPI()   COMENTAMOS ESTA LINEA

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
    "password": "1234"},
  "Lolo": {
    "username": "Lolo",
    "name": "Lolo Perez",
    "email": "lolo@gmail.com",
    "disable": True,
    "password": "1235"}
}

def search_user_db(username:str):
  if username in users_db:
    return UserDB(**users_db[username])

def search_user(username:str):
  if username in users_db:
    return User(**users_db[username])

async def current_user(token:str = Depends(oauth2)):
  user = search_user(token)
  if not user:
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Credenciales de autenticacion incorrectas o inválidas", headers={"WWW-Authenticate":"Bearer"}) # protocolo extricto. Una falta de ortografía y todo mal
  if user.disable:
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Usuario Inactivo")
  return user

# Operacion de autenticacion
@router.post("/login")
async def login(form: OAuth2PasswordRequestForm = Depends()):
  user_db = users_db.get(form.username)
  if not user_db:
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="El usuario es incorrecto")
  
  user = search_user_db(form.username)
  if not form.password == user.password:
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="La contraseña es incorrecta")
  
  return {"access_token":user.username,"token_type":"bearer"} # "token_type":"bearer" es parte del protocolo de seguridad

@router.get("/users/me")
async def me(user:User = Depends(current_user)):
  return user