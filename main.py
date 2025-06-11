from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from sqlalchemy import func, distinct
import os

from Demografia.models import Demografia, Zgony  # Upewnij się, że importujesz właściwe modele
from Demografia.Database import get_db
from Demografia import crud  # zakładam, że masz tam logikę do urodzeń

app = FastAPI()
templates = Jinja2Templates(directory="templates")  # Upewnij się, że folder "templates" jest obok tego pliku


@app.get("/", response_class=HTMLResponse)
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


@app.get("/demografia/", response_class=HTMLResponse)
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


@app.get("/zgony/", response_class=HTMLResponse)
def zgony(
    request: Request,
    rok: int,
    wiek: str,
    db: Session = Depends(get_db)
):
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
        db.query(Zgony.wojewodztwa, func.sum(kolumna).label("suma_zgonow"))
        .filter(Zgony.rok == rok)
        .group_by(Zgony.wojewodztwa)
        .all()
    )

    zgony_wojewodztwa = [{"wojewodztwo": r[0], "suma_zgonow": r[1]} for r in results]

    wiek_display = "85+" if wiek == "85" else wiek.replace("_", "-")

    context = {
        "request": request,
        "zgony_wojewodztwa": zgony_wojewodztwa,
        "rok": rok,
        "wiek": wiek_display
    }

    return templates.TemplateResponse("zgony_fragment.html", context)


@app.get("/urodzenia", response_class=HTMLResponse)
def get_urodzenia(
    request: Request,
    wojewodztwo: str,
    rok: int,
    db: Session = Depends(get_db)
):
    urodzenia = crud.get_urodzenia_by_wojewodztwo_i_rok(db, wojewodztwo, rok)

    context = {
        "request": request,
        "urodzenia": urodzenia,
        "wojewodztwo": wojewodztwo,
        "rok": rok
    }

    return templates.TemplateResponse("urodzenia_table.html", context)
