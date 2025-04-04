import os
import shutil
import zipfile
import tabula
import pandas as pd
import logging
from utils.file_utils import get_downloads_folder

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TransformService:
    def __init__(self, pdf_identifier: str = "anexo_1", 
                 output_csv: str = "dados_transformados.csv", 
                 output_zip: str = "Teste_RafaelSantana.zip", 
                 extract_to: str = "temp_extracted"):
        try:
            self.downloads_folder = get_downloads_folder()
            
            self.output_dir = os.path.join(os.path.dirname(__file__), "..", "..", "output")
            os.makedirs(self.output_dir, exist_ok=True)
            
            self.pdf_identifier = pdf_identifier

            self.output_csv = os.path.join(self.output_dir, output_csv)
            # Place the final zip in the Downloads folder
            self.output_zip = os.path.join(self.downloads_folder, output_zip)
            self.extract_to = os.path.join(self.output_dir, extract_to)
            
            logger.info(f"Final ZIP será salvo em: {self.output_zip}")
        except Exception as e:
            logger.error(f"Erro ao configurar diretórios: {str(e)}")
            logger.info("Usando diretório padrão como fallback")
            self.output_dir = os.path.join(os.path.dirname(__file__), "..", "..", "output")
            os.makedirs(self.output_dir, exist_ok=True)
            
            self.pdf_identifier = pdf_identifier

            self.output_csv = os.path.join(self.output_dir, output_csv)
            self.output_zip = os.path.join(self.output_dir, output_zip)
            self.extract_to = os.path.join(self.output_dir, extract_to)
        
    def extract_pdf_from_zip(self, zip_path: str):
        logger.info(f"Extraindo arquivos de {zip_path}")
        if not os.path.exists(zip_path):
            raise FileNotFoundError(f"Arquivo ZIP não encontrado: {zip_path}")
        
        os.makedirs(self.extract_to, exist_ok=True)
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(self.extract_to)
        return [os.path.join(self.extract_to, f) for f in os.listdir(self.extract_to)]

    def transform_pdf_to_csv(self, pdf_path: str) -> pd.DataFrame:
        logger.info(f"Transformando PDF: {pdf_path}")
        try:
            dataframes = tabula.read_pdf(
                pdf_path,
                pages='all',
                multiple_tables=True,
                guess=True,
                pandas_options={
                    'header': None,
                    'dtype': str
                }
            )
            
            if not dataframes:
                raise ValueError("Não foi possível extrair tabelas do PDF")
                
            df = pd.concat(dataframes, ignore_index=True)
            
            df = df.dropna(how='all')
            df = df.fillna('')
            
            df.columns = df.iloc[0]
            df = df.iloc[1:].reset_index(drop=True)
            
            df.columns = [str(col).strip().upper() for col in df.columns]
            
            return df
            
        except Exception as e:
            raise Exception(f"Erro ao processar o PDF: {str(e)}")

    def process_transform(self, zip_input_path: str) -> str:
        try:
            logger.info("Iniciando processo de transformação")
            extracted_files = self.extract_pdf_from_zip(zip_input_path)
            
            pdf_file = next(
                (f for f in extracted_files 
                 if f.lower().endswith(".pdf") and 
                 self.pdf_identifier in os.path.basename(f).lower()),
                None
            )
            
            if not pdf_file:
                raise FileNotFoundError("PDF com o identificador especificado não foi encontrado.")

            df = self.transform_pdf_to_csv(pdf_file)
         
            if df.empty:
                raise ValueError("A tabela extraída do PDF está vazia.")

            column_mappings = {
                'OD': 'Seg. Odontológica',
                'AMB': 'Seg. Ambulatorial'
            }
            
            df.replace(column_mappings, inplace=True)

            df.to_csv(self.output_csv, index=False, encoding='utf-8')
            logger.info(f"CSV gerado: {self.output_csv}")

            try:
                with zipfile.ZipFile(self.output_zip, 'w') as zipf:
                    zipf.write(self.output_csv, arcname=os.path.basename(self.output_csv))
                
                logger.info(f"ZIP gerado com sucesso: {self.output_zip}")
            except PermissionError:
                logger.error(f"Erro de permissão ao criar ZIP no diretório de Downloads. Tentando diretório alternativo.")
                fallback_zip = os.path.join(self.output_dir, os.path.basename(self.output_zip))
                with zipfile.ZipFile(fallback_zip, 'w') as zipf:
                    zipf.write(self.output_csv, arcname=os.path.basename(self.output_csv))
                self.output_zip = fallback_zip
                logger.info(f"ZIP gerado no local alternativo: {self.output_zip}")
            except Exception as e:
                logger.error(f"Erro ao gerar ZIP: {str(e)}")
                raise

            if os.path.exists(self.extract_to):
                shutil.rmtree(self.extract_to)
            if os.path.exists(self.output_csv):
                os.remove(self.output_csv)
                
            return self.output_zip
            
        except Exception as e:
            if os.path.exists(self.extract_to):
                shutil.rmtree(self.extract_to)
            if os.path.exists(self.output_csv):
                os.remove(self.output_csv)
            raise e