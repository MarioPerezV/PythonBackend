from fastapi import FastAPI
from pydantic import BaseModel # Definir una entidad que nos sirva para devolver users con un JSON
"""
IMPORTANTE: *** OJO ***
Acceder al servidor local, ingresar por la terminal: fastapi dev users.py (tambien sirve: uvicorn users:app --reload)
En Thunder Client: 
  Para agregar un usuario con post http://127.0.0.1:8000/user/ a traves de un JSON en la pestaña JSON.
    La respuesta (Response) es null, pero se agrega y se puede comprobar así:
      Para ver la lista de usuarios http://127.0.0.1:8000/users/
"""
app = FastAPI()
# Entidad user
class User(BaseModel): # Click para la documentacion de la herencia BaseModel
  id: int
  user_name: str
  last_name: str
  url: str
  age: int
  
users_list=[User(id=1, user_name= "ecomaeirl", last_name= "Perez", url= "https://www.linkedin.com/in/ecomaeirl/", age=7),
            User(id=2, user_name="Mario", last_name="Vilchez", url="https://github.com/MarioPerezV", age=37),
            User(id=3, user_name="Brais", last_name="Moure", url="https://www.youtube.com/watch?v=_y9qQZXE24A", age=48),]

# Pagina users

@app.get("/usersjson")
async def usersjson():
    return [{"id":"1", "user_name":"ecomaeirl", "last_name":"Perez", "url":"https://www.linkedin.com/in/ecomaeirl/", "age":7},
            {"id":"2", "user_name":"Mario", "last_name":"Vilchez", "url":"https://github.com/MarioPerezV", "age":37},
            {"id":"3", "user_name":"Brais", "last_name":"Moure", "url":"https://www.youtube.com/watch?v=_y9qQZXE24A", "age":48}]

# Esta es la funcion del archivo completo users.py
@app.get("/users")
async def users():
  return users_list

# Consulta por un usuario específico por id (path)
@app.get("/user/{id}")
async def user(id: int): # id de tipo entero
  return search_user(id)

# READ (CRUD), Query 
@app.get("/user/")
async def user(id: int): # id de tipo entero
  return search_user(id)

def search_user(id: int):
  users=filter(lambda user: user.id == id, users_list) # Funcion de orden superior que reemplza un ciclo for
  try:
    return list(users)[0]
  except:
    return {"Error":"Usuario No encontrado"}
  
# CRUD (Create) Agregar con post
@app.post("/user/")
async def user(user: User):
  if type(search_user(user.id)) == User:
    return {"Error":"EL Usuario ya existe"}
  else:
    users_list.append(user)
    
  # CRUD (Update) Actualizar la lista de usuarios con PUT desde la pestaña JSON en Thunder Client
@app.put("/user/")
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
@app.delete("/user/{id}")
async def user(id: int):
    for index, saved_user in enumerate(users_list):
      if saved_user.id == id:
        del users_list[index]
        found=True
#       
def search_user(id: int):
  users=filter(lambda user: user.id == id, users_list) # Funcion de orden superior que reemplza un ciclo for
  try:
    return list(users)[0]
  except:
    return {"Error":"Usuario No encontrado"}

  """
  Pasos para subir repositorios a github
  git init
  git remote add origin https://github.com/MarioPerezV/PythonBackend.git
  git status
  
  """