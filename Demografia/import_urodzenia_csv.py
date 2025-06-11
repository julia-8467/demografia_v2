import csv
from sqlalchemy.orm import Session
from Demografia.models import Urodzenia


def import_urodzenia_csv_to_db(db: Session, csv_path: str):
    with open(csv_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        headers = next(reader)

        for row in reader:
            urodzenia = Urodzenia(
                wojewodztwa=row[0],
                rok=int(row[1]),
                liczba_ogolem=int(row[2]),
                chlopcy=int(row[3]),
                dzieczeta=int(row[4])
            )
            db.add(urodzenia)

        db.commit()
