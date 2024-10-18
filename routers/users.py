from fastapi import APIRouter, HTTPException
from pydantic import BaseModel # Definir una entidad que nos sirva para devolver users con un JSON
"""
Las explicaciones del codigo en "LEEME"
"""
router = APIRouter(prefix="/users",tags=["users"], responses={404: {"mensaje":"No encontrado"}})
# tags es para la documentacion de Swegger o Redoc
# Entidad user
class User(BaseModel): # Click para la documentacion de la herencia BaseModel
  id: int
  username: str
  last_name: str
  url: str
  age: int
  
users_list=[User(id=1, username= "ecomaeirl", last_name= "Perez", url= "https://www.linkedin.com/in/ecomaeirl/", age=7),
            User(id=2, username="Mario", last_name="Vilchez", url="https://github.com/MarioPerezV", age=37),
            User(id=3, username="Brais", last_name="Moure", url="https://www.youtube.com/watch?v=_y9qQZXE24A", age=48),]

# Pagina users
@router.get("/usersjson")
async def usersjson():
    return [{"id":"1", "user_name":"ecomaeirl", "last_name":"Perez", "url":"https://www.linkedin.com/in/ecomaeirl/", "age":7},
            {"id":"2", "user_name":"Mario", "last_name":"Vilchez", "url":"https://github.com/MarioPerezV", "age":37},
            {"id":"3", "user_name":"Brais", "last_name":"Moure", "url":"https://www.youtube.com/watch?v=_y9qQZXE24A", "age":48}]

# Esta es la funcion del archivo completo users.py
@router.get("/")
async def users():
  return users_list

# Consulta por un usuario específico por id (path)
@router.get("/{id}")
async def user(id: int): # id de tipo entero
  return search_user(id)

# READ (CRUD), también Query 
@router.get("/")
async def user(id: int): # id de tipo entero
  return search_user(id)

def search_user(id: int):
  users=filter(lambda user: user.id == id, users_list) # Funcion de orden superior que reemplza un ciclo for
  try:
    return list(users)[0]
  except:
    return {"Error":"Usuario No encontrado"}
  
# CRUD (Create) Agregar con post
@router.post("/",response_model=User,status_code=201) # status_code reemplaza el codigo 200 por el código create(201)
async def user(user: User):
  if type(search_user(user.id)) == User:
    raise HTTPException(status_code=404, detail="El usuario ya existe.") # Propagar o lanzar una excepcion, cambio de return por raise (raise se utilixa para las excepciones) envía un 404 con el detalle del excepciones
    # return HTTPException(status_code=204, detail="El usuario ya existe.") # Que devuelva un mensaje de FastApi
    # return {"Error":"EL Usuario ya existe"}   También funciona, pero más basico
  users_list.append(user) # también se puede agregar un else con identacion
  return user

  # CRUD (Update) Actualizar la lista de usuarios con PUT desde la pestaña JSON en Thunder Client
@router.put("/")
async def user(user: User):
  found=False
  for index, saved_user in enumerate(users_list):
    if saved_user.id == id:
      users_list[index]=user
      found=True
  
  if not found:
    return {"Error":"No se ha eliminado el usuario"}
  else:
    return user

#CRUD (Delete) No es necesario un JSON, solo agregar el id en la direccion http://127.0.0.1:8000/user/3
@router.delete("/{id}")
async def user(id: int):
  found=False
  for index, saved_user in enumerate(users_list):
    if saved_user.id == id:
      del users_list[index]
      found=True
  if not found:
    return {"Error": "No se ha eliminado el usuario"}
#       
def search_user(id: int):
  users=filter(lambda user: user.id == id, users_list) # Funcion de orden superior que reemplza un ciclo for
  try:
    return list(users)[0]
  except:
    return {"Error":"Usuario No encontrado"}