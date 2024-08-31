import uvicorn
from fastapi import FastAPI
from app.api.router import router as api_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="Desafio Técnico Desarrollador FullStack Adereso"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# Incluir el router global que agrupa todas las categorías
app.include_router(api_router, prefix="/api")

@app.get("/")
async def root():
    return {"message": "Desafio Técnico Desarrollador FullStack Adereso"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
