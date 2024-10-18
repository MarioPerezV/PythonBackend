from fastapi import APIRouter

router = APIRouter(prefix="/products",tags=["products"], responses={404: {"mensaje":"No encontrado"}})
# tags es para la documentacion de Swegger o Redoc

product_list=[{"id":"1", "product_name":"1", "cant":7},
            {"id":"2", "product_name":"2", "cant":37},
            {"id":"3", "product_name":"3", "cant":48}]

@router.get("/")    # @router.get("/products")  ANTES, ya no es necesario
async def products():
    return product_list
    
@router.get("/{id}")
async def products(id:int):
    return product_list[id]