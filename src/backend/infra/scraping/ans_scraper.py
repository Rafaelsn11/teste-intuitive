import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from zipfile import ZipFile
import tempfile
import logging
from utils.file_utils import get_downloads_folder

logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

class ANSScraperService:
    def __init__(self, 
                 ans_url: str = "https://www.gov.br/ans/pt-br/acesso-a-informacao/participacao-da-sociedade/atualizacao-do-rol-de-procedimentos", 
                 zip_filename: str = "anexos.zip"):
        self.ans_url = ans_url
        self.base_url = "https://www.gov.br"
        self.downloads_folder = get_downloads_folder()
        self.zip_path = os.path.join(self.downloads_folder, zip_filename)
        
    def get_pdf_links(self) -> list:
        logger.info("Acessando a página da ANS para buscar PDFs.")
        response = requests.get(self.ans_url, timeout=30)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        pdf_links = []
        
        logger.info("Buscando todos os links na página...")
        for a in soup.find_all("a", href=True):
            href = a["href"]
            text = a.get_text().strip().lower()
            logger.debug(f"Link encontrado - Texto: {text}, Href: {href}")
            
            if href.lower().endswith(".pdf") and ("anexo" in text.lower() or "anexo" in href.lower()):
                full_url = href if href.startswith("http") else urljoin(self.base_url, href)
                pdf_links.append((text, full_url))
        
        if not pdf_links:
            raise Exception("Nenhum PDF de anexo encontrado.")
            
        pdf_links.sort(key=lambda x: x[0])
        
        final_links = [url for _, url in pdf_links]
        
        logger.info(f"Total de PDFs encontrados: {len(final_links)}")
        logger.info(f"Links encontrados: {final_links}")
        
        return final_links
    
    def download_pdf(self, url: str, filename: str, temp_dir: str) -> str:
        logger.info(f"Baixando {url} para {filename}.")
        response = requests.get(url, stream=True, timeout=30)
        response.raise_for_status()
        file_path = os.path.join(temp_dir, filename)
        with open(file_path, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
        logger.info(f"Arquivo salvo: {file_path}")
        return file_path
    
    def create_zip(self, files: list) -> str:
        logger.info("Criando arquivo ZIP.")
        with ZipFile(self.zip_path, "w") as zipf:
            for file in files:
                zipf.write(file, os.path.basename(file))
        logger.info(f"ZIP criado: {self.zip_path}")
        return self.zip_path
    
    def run(self) -> dict:
        result = {"status": "success", "output_file": ""}
        try:
            pdf_links = self.get_pdf_links()
            
            if len(pdf_links) < 2:
                raise Exception(f"Número insuficiente de anexos encontrados. Encontrados: {len(pdf_links)}")
                
            with tempfile.TemporaryDirectory() as temp_dir:
                logger.info(f"Diretório temporário criado: {temp_dir}")
                
                files_to_zip = []
                for i, url in enumerate(pdf_links[:2], 1):
                    filename = f"anexo_{i}.pdf"
                    file_path = self.download_pdf(url, filename, temp_dir)
                    files_to_zip.append(file_path)
                    
                zip_file = self.create_zip(files_to_zip)
                result["output_file"] = zip_file
                
            logger.info("Diretório temporário removido.")
        except Exception as e:
            logger.error(f"Erro durante o processo: {e}")
            result = {"status": "error", "message": str(e)}
        return result
    
    @staticmethod
    def run_as_script() -> dict:
        service = ANSScraperService()
        result = service.run()
        if result["status"] == "success":
            logger.info("Processo concluído com sucesso.")
        else:
            logger.error("Ocorreu um erro no processo.")
        return result
