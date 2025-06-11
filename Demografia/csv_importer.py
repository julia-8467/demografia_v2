import csv
from sqlalchemy.orm import Session
from Demografia.models import Demografia

def import_csv_to_db(db: Session, csv_path: str):
    with open(csv_path, newline='', encoding='utf-8-sig') as csvfile:
        reader = csv.DictReader(csvfile,delimiter=',')
        for row in reader:
            record = Demografia(
                wojewodztwa=row['Wojewodztwa'],
                rok=int(row['Rok']),
                liczba_ludnosci=int(row['Ogolem']),
                mezczyzni=int(row['Mezczyzni']),
                kobiety=int(row['Kobiety']),
            )
            db.add(record)
        db.commit()
