from fastapi import FastAPI
from routers import products, users, basic_auth_users, jwt_auth_users # Acceso a los ficheros
from fastapi.staticfiles import StaticFiles

app = FastAPI()
# Routers
app.include_router(products.router) # Hemos incluido en nuestro archivo principal el router de products
app.include_router(users.router)
app.include_router(jwt_auth_users.router)
app.include_router(basic_auth_users.router)
# FORMA DE EXPONER IMAGENES U OTROS ARCHIVOS ESTÁTICOS
app.mount("/static", StaticFiles(directory="static"), name="static") # Forma de exponer Archivos estaticos como imagenes
# ejemplo: http://127.0.0.1:8000/static/images/Leon.jpg

# Pagina principal (main)
@app.get("/")
async def root():
  return "¡Hello FastApi!"

# http://127.0.0.1:8000/url

# Pagina login
@app.get("/login2")
async def login2():
    return {"User_name":"ecomaeirl"}

# Pagina linkedin
@app.get("/url")
async def url():
    return {"url":"https://www.linkedin.com/in/ecomaeirl/"}

