
from sqlalchemy.orm import Session
from .models import Urodzenia

def get_urodzenia_by_wojewodztwo_i_rok(db: Session, wojewodztwo: str, rok: int):
    return db.query(Urodzenia).filter(
        Urodzenia.wojewodztwa == wojewodztwo,
        Urodzenia.rok == rok
    ).all()
