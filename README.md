# OCR_Marksheet_Project
# AI Marksheet Extraction API

## Features
- Image & PDF support
- LLM based structuring
- Confidence scoring
- Concurrent handling

## Setup

pip install -r requirements.txt

## Run

uvicorn app.main:app --reload
open another terminal
streamlit run webapp.py

## API

POST /extract
Form-data -> file

## Confidence

Final confidence =  
0.6 × LLM certainty  
0.4 × OCR quality

## Samples
See /samples
