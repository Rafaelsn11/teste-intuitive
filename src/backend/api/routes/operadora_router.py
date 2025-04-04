from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException, Query

from infra.services.operadora_service import OperadoraService

router = APIRouter()

@router.get("/operadoras/")
async def search_operadoras(query: str,
        operadora_service: OperadoraService = Depends()):
    
    if not query:
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail="Parâmetro query parameter é obrigatório.")
    return operadora_service.search_operadoras(query)