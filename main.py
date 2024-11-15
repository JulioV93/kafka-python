#Instalar FastAPI: pip install "fastapi[all]"
#Inicia el servidor: uvicorn main:app --reload

from fastapi import FastAPI
from routers import producer, consumer, admin
from fastapi.staticfiles import StaticFiles

#Se llama la funcion especifica del modulo del Framework

app = FastAPI()

#Routers

app.include_router(producer.router)
app.include_router(consumer.router)
app.include_router(admin.router)

#Recursos estaticos
app.mount("/static", StaticFiles(directory="static"), name="static")

print(app)

#Siempre que llamamos a un servidor, la operación debe ser asincrona.

#La asincronia hace que se deba esperar por que la operación termine y la aplicación pueda continuar haciendo otras tareas mientras se termine la operación solicitada.

#uvicorn es un modulo de servidor que disponibiliza FastAPI, trabaja en 127.0.0.1:8000

#FastAPI tiene integrado Swagger para generar la documentación de las APIs de manera automatica. http://127.0.0.1:8000/docs

#FastAPI tiene integrado Redoc para generar la documentación de las APIs de manera automatica. http://127.0.0.1:8000/redoc

@app.get("/")
async def root():
    return "¡Hola FastAPI!"