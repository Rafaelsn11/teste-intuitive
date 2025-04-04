from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException

from infra.scraping.ans_scraper import ANSScraperService

router = APIRouter()

@router.post("/ans-download/", status_code=HTTPStatus.CREATED)
async def extract_data(ans_scraper_service: ANSScraperService = Depends()):
    
    try:
        result_zip = ans_scraper_service.run_as_script()
    except Exception as e:
        raise HTTPException(status_code=HTTPStatus.INTERNAL_SERVER_ERROR, detail=str(e))

    return {"message": "Processamento concluído.", "output_zip": result_zip}