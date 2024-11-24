from pydantic import BaseModel

class PredictIn(BaseModel):
    id: str
    timestamp: str
    대출금액: int
    대출기간: str
    근로기간: str
    주택소유상태: str
    연간소득: int
    부채_대비_소득_비율: float
    총계좌수: int
    대출목적: str
    최근_2년간_연체_횟수: int
    총상환원금: int
    총상환이자: float
    총연체금액: float
    연체계좌수: float
    대출등급: str

class PredictOut(BaseModel):
    loan_grade: str 