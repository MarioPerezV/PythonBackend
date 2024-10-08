from fastapi import FastAPI
"""
Instalacion completa de Fastapi: pip install "fastapi[all]"
Manual fastapi: https://fastapi.tiangolo.com/#run-it
RECORDAR ESTAR DENTRO DE LA CARPETA QUE CONTIENE EL ARCHIVO main.py
Para acceder al servidor local ingresar por la terminal: fastapi dev main.py (tambien sirve: uvicorn main:app --reload)
Para detener el servicor local Ctrl + C
url local http://127.0.0.1:8000
Documentacion oficial: https://fastapi.tiangolo.com/es
Documentacion (docs) de las funciones FastApi creadas hasta el momento(Swagger UI) http://127.0.0.1:8000/docs
Documentacion con Redocly: http://127.0.0.1:8000/redoc (cualquiera de las dos funciona y me gusta mas esta)
Extencion de VSCode Thunder Client
"""
app = FastAPI()
# Pagina principal (main)
@app.get("/")
async def root():
  return "¡Hello FastApi!"

# Pagina login
@app.get("/login")
async def login():
    return {"User_name":"ecomaeirl"}

# Pagina linkedin
@app.get("/url")
async def url():
    return {"url":"https://www.linkedin.com/in/ecomaeirl/"}

