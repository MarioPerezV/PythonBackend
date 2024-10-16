from fastapi import FastAPI
from routers import products, users # Acceso a los ficheros
from fastapi.staticfiles import StaticFiles

app = FastAPI()

app.include_router(products.router) # Hemos incluido en nuestro archivo principal el router de products
app.include_router(users.router)
app.mount("/static", StaticFiles(directory="static"), name="static")  # Forma de exponer Archivos estaticos como imagenes
# ejemplo: http://127.0.0.1:8000/static/images/Leon.jpg

# Pagina principal (main)
@app.get("/")
async def root():
  return "¡Hello FastApi!"

# http://127.0.0.1:8000/url

# Pagina login
@app.get("/login")
async def login():
    return {"User_name":"ecomaeirl"}

# Pagina linkedin
@app.get("/url")
async def url():
    return {"url":"https://www.linkedin.com/in/ecomaeirl/"}

