from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.routes import process_transform_router, ans_router, operadora_router
import uvicorn

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(process_transform_router.router, tags=["Transformação de dados"])
app.include_router(ans_router.router, tags=["ANS"])
app.include_router(operadora_router.router, tags=["Operadoras"])

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)