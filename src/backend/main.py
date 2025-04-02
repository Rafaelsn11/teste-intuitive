from fastapi import FastAPI
from api.routes import process_transform_router, ans_router
import uvicorn

app = FastAPI()

app.include_router(process_transform_router.router, tags=["Transformação de dados"])
app.include_router(ans_router.router, tags=["ANS"])

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)