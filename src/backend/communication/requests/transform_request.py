from pydantic import BaseModel
import os
from utils.file_utils import get_downloads_folder

default_zip_path = os.path.join(get_downloads_folder(), "anexos.zip")

class TransformRequest(BaseModel):
    zip_input_path: str = default_zip_path
    pdf_identifier: str = "anexo_1"
    output_csv: str = "dados_transformados.csv"
    output_zip: str = "Teste_RafaelSantana.zip"
    extract_to: str = "temp_extracted"