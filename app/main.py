from fastapi import FastAPI, UploadFile, File, HTTPException
from app.utils import process_file
from app.services import extract_data_from_image
from app.schemas import MarksheetResponse

app = FastAPI(title="AI Marksheet Extractor")

@app.post("/extract", response_model=MarksheetResponse)
async def extract_marksheet(file: UploadFile = File(...)):
    # Validate file type
    if file.content_type not in ["application/pdf", "image/jpeg", "image/png", "image/webp"]:
        raise HTTPException(status_code=400, detail="Invalid file type")
    
    try:
        # Read and process file
        file_bytes = await file.read()
        image = process_file(file_bytes, file.content_type)
        
        # Extract data
        data = extract_data_from_image(image)
        return data
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="AI processing failed: " + str(e))