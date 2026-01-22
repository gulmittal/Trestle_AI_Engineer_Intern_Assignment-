import google.generativeai as genai
import os
import json
from dotenv import load_dotenv

load_dotenv() 

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def extract_data_from_image(image):
    model = genai.GenerativeModel('gemini-2.5-flash')

    prompt = """
You are an expert Document Intelligence AI specialized in extracting academic data. 
Analyze the provided image of a marksheet or grade card.

### EXTRACTION OBJECTIVES:
1. **Candidate Details:** Extract Name, Roll Number, Registration/Enrollment No, and Institute/School Name.
2. **Subject Performance:** Extract a list of all subjects/courses.
   - For 'subject_name': Use the full course title.
   - For 'max_marks': Extract the maximum marks OR course credits (if it's a GPA system).
   - For 'obtained_marks': Extract the total marks obtained. 
     * NOTE: If the marksheet splits marks into Theory/Practical/Oral (like Image 3), prioritize the 'Total' column for that subject.
   - For 'grade': Extract the Letter Grade (e.g., A, B+, O) if present.
3. **Overall Result:** Extract the final status (Pass/Fail), the CGPA/SGPA, or the Division (e.g., "First Division").

### CONFIDENCE SCORING:
For every extracted field, provide a `confidence` score (0.0 to 1.0) based on:
- **Legibility:** Is the text clear or blurry? (Image 1 is slightly curved/blurry -> lower confidence).
- **Ambiguity:** Is it clear which header belongs to which column?

### JSON OUTPUT FORMAT:
Return **ONLY** valid JSON. Do not include markdown formatting (like ```json).
Use this exact schema:
{
  "candidate": {
    "name": "string or null",
    "roll_no": "string or null", 
    "registration_no": "string or null",
    "institute_name": "string or null",
    "confidence": float
  },
  "subjects": [
    {
      "subject_name": "string",
      "max_marks": float or null, 
      "obtained_marks": float or null,
      "grade": "string or null",
      "confidence": float
    }
  ],
  "overall_result": "string (e.g., 'PASS', 'First Division')",
  "overall_score": "string (e.g., '85%', '9.2 SGPA')",
  "issue_date": "string or null"
}
"""

    response = model.generate_content([prompt, image])

    json_text = response.text.replace("```json", "").replace("```", "").strip()
    return json.loads(json_text)