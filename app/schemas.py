from pydantic import BaseModel, Field
from typing import List, Optional, Union

class SubjectMark(BaseModel):
    subject_name: str
    max_marks: Optional[float] = None
    obtained_marks: Union[float, str] 
    grade: Optional[str] = None
    confidence: float
    
class CandidateDetails(BaseModel):
    name: Optional[str] = None
    roll_no: Optional[str] = None
    institute_name: Optional[str] = None
    confidence: float

class MarksheetResponse(BaseModel):
    candidate: CandidateDetails
    subjects: List[SubjectMark]
    overall_result: Optional[str] = None
    overall_percentage: Optional[str] = None
    issue_date: Optional[str] = None