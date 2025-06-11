from pydantic import BaseModel

class RegionOut(BaseModel):
    wojewodztwa: str
    liczba_ludnosci: int

    class Config:
        orm_mode = True