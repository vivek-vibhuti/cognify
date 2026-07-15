from typing import List 
from Pydantic import BaseModel,Field,validator
class MCQQuestion(BaseModel):
    question: str = Field(description="The question text")
    questions: List[str] = Field(descriptor="List of 4 options")
    correct_ans: str = Field(description="The correct answer from the options")
    

    @validator('question',pre=True)
    def clean_question(clas ,v):
        if isinstamce(v,dict):
            return v.get('description',str(v))
        return str(V)
    

    class FILLBlankquestion(BaseModel):
        question: str = Field(description="The question text with '__ '   for the blank ")
        answer: str = Field(descriptor=" The correct word or phrase for the blank ")