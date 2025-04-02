from http import HTTPStatus
from fastapi import APIRouter, Depends, HTTPException
import os
from infra.data_processing.transform_service import TransformService
from communication.requests.transform_request import TransformRequest

router = APIRouter()

@router.post("/extract-data/", status_code=HTTPStatus.CREATED)
async def extract_data(data: TransformRequest, transform_service: TransformService = Depends()):
    """
    Endpoint para extrair dados de um PDF contido em um arquivo ZIP e realizar a transformação.
    Espera receber um JSON com os seguintes campos:
      - zip_input_path: Caminho para o arquivo ZIP de entrada.
      - pdf_identifier: (Opcional) Identificador para localizar o PDF desejado (padrão: "anexo_1").
      - output_csv: (Opcional) Nome do arquivo CSV gerado (padrão: "dados_transformados.csv").
      - output_zip: (Opcional) Nome do arquivo ZIP de saída (padrão: "Teste_SeuNome.zip").
      - extract_to: (Opcional) Pasta para extração dos arquivos (padrão: "temp_extracted").
    """
    if not os.path.exists(data.zip_input_path):
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail="Caminho do ZIP inválido ou não informado.")

    try:
        result_zip = transform_service.process_transform(data.zip_input_path)
    except Exception as e:
        raise HTTPException(status_code=HTTPStatus.INTERNAL_SERVER_ERROR, detail=str(e))

    return {"message": "Processamento concluído.", "output_zip": result_zip}