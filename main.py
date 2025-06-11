from fastapi import FastAPI, Depends, HTTPException, APIRouter, Request
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from sqlalchemy import func
import os

from Demografia.import_zgony_csv_to_db import import_zgony_csv_to_db
from Demografia.import_urodzenia_csv import import_urodzenia_csv_to_db
from Demografia.models import Demografia, Zgony
from Demografia.csv_importer import import_csv_to_db
from Demografia.Database import get_db
from Demografia.mapa import generuj_mape
from Demografia import crud

app = FastAPI()
router = APIRouter()
templates = Jinja2Templates(directory="templates")

@app.post("/import-csv")
def import_csv(db: Session = Depends(get_db)):
    import_csv_to_db(db, "D:/Users/julli/Studia/VIsemestr/Chmury/Dane/Ludność_woj/pl_lud_2017_v2.csv")
    return {"status": "Dane zaimportowane pomyślnie"}

@router.post("/import-zgony")
def import_zgony_csv(db: Session = Depends(get_db)):
    import_zgony_csv_to_db(db, "D:/Users/julli/Studia/VIsemestr/Chmury/Dane/Zgony/Zgony_2010.csv")
    import_zgony_csv_to_db(db, "D:/Users/julli/Studia/VIsemestr/Chmury/Dane/Zgony/Zgony_2002.csv")
    return {"status": "Dane zaimportowane pomyślnie"}

@router.post("/import-urodzenia")
def import_urodzenia_csv(db: Session = Depends(get_db)):
    import_urodzenia_csv_to_db(db, "D:/Users/julli/Studia/VIsemestr/Chmury/Dane/Urodzenia/pl_uro_2023_00_49.csv")
    import_urodzenia_csv_to_db(db, "D:/Users/julli/Studia/VIsemestr/Chmury/Dane/Urodzenia/pl_uro_2017_00_49.csv")
    import_urodzenia_csv_to_db(db, "D:/Users/julli/Studia/VIsemestr/Chmury/Dane/Urodzenia/pl_uro_2010_00_49.csv")
    import_urodzenia_csv_to_db(db, "D:/Users/julli/Studia/VIsemestr/Chmury/Dane/Urodzenia/pl_uro_2002_00_49.csv")
    return {"status": "Dane zaimportowane pomyślnie"}

@router.get("/mapa")
def get_map():
    output_path = "D:/Users/julli/Studia/VIsemestr/Chmury/static/mapa.bmp"
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    generuj_mape(output_path)
    return FileResponse(output_path, media_type="image/bmp")

@router.delete("/usun-wszystkie", tags=["Admin"])
def usun_wszystkie_dane(db: Session = Depends(get_db)):
    try:
        liczba_usunietych = db.query(Zgony).delete()
        db.commit()
        return {"status": "sukces", "usuniete_rekordy": liczba_usunietych}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Błąd usuwania danych: {str(e)}")

from sqlalchemy import distinct
from Demografia.models import Demografia  # lub inny model, który zawiera województwa

@app.get('/index/', response_class=HTMLResponse)
def index(request: Request, db: Session = Depends(get_db)):
    wojewodztwa = (
        db.query(distinct(Demografia.wojewodztwa))
        .order_by(Demografia.wojewodztwa)
        .all()
    )
    wojewodztwa_dict = [{"wojewodztwo": w[0]} for w in wojewodztwa]

    context = {
        "request": request,
        "wojewodztwa": wojewodztwa_dict
    }
    return templates.TemplateResponse("index.html", context)


@router.get("/demografia/", response_class=HTMLResponse)
def get_demografia(
    request: Request,
    wojewodztwo: str,
    rok: int,
    db: Session = Depends(get_db)
):
    result = (
        db.query(Demografia)
        .filter(Demografia.wojewodztwa == wojewodztwo, Demografia.rok == rok)
        .first()
    )

    context = {
        "request": request,
        "wojewodztwo": wojewodztwo,
        "rok": rok,
        "dane": result
    }

    return templates.TemplateResponse("demografia_fragment.html", context)

@router.get("/zgony/", response_class=HTMLResponse)
def zgony(request: Request, rok: int = 2020, wiek: str = "0_4", db: Session = Depends(get_db)):
    kolumna_wiekowa = f"p{wiek}"

    dozwolone_kolumny = {
        "p0_4", "p5_9", "p10_14", "p15_19", "p20_24", "p25_29",
        "p30_34", "p35_39", "p40_44", "p45_49", "p50_54", "p55_59",
        "p60_64", "p65_69", "p70_74", "p75_79", "p80_84", "p85"
    }

    if kolumna_wiekowa not in dozwolone_kolumny:
        raise HTTPException(status_code=400, detail="Nieprawidłowy zakres wieku")

    kolumna = getattr(Zgony, kolumna_wiekowa)

    results = (
        db.query(
            Zgony.wojewodztwa,
            func.sum(kolumna).label("suma_zgonow")
        )
        .filter(Zgony.rok == rok)
        .group_by(Zgony.wojewodztwa)
        .all()
    )

    zgony_wojewodztwa = [{"wojewodztwo": r[0], "suma_zgonow": r[1]} for r in results]

    if wiek == "85":
        wiek_display = "85+"
    else:
        wiek_display = wiek.replace("_", "-")

    context = {
        "request": request,
        "zgony_wojewodztwa": zgony_wojewodztwa,
        "rok": rok,
        "wiek": wiek_display
    }

    return templates.TemplateResponse("zgony_fragment.html", context)

@router.get("/urodzenia", response_class=HTMLResponse)
def get_urodzenia(
    request: Request,
    wojewodztwo: str,
    rok: int,
    db: Session = Depends(get_db)
):
    urodzenia = crud.get_urodzenia_by_wojewodztwo_i_rok(db, wojewodztwo, rok)
    return templates.TemplateResponse(
        "urodzenia_table.html",
        {"request": request, "urodzenia": urodzenia}
    )


app.include_router(router)
