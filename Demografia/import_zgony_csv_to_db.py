import csv
from sqlalchemy.orm import Session
from Demografia.models import Zgony


def import_zgony_csv_to_db(db: Session, csv_path: str):
    with open(csv_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        headers = next(reader)

        for row in reader:
            zgony = Zgony(
                wojewodztwa=row[0],
                rok=int(row[1]),
                liczba_ogolem=int(row[2]),
                p0_4=int(row[3]),
                p5_9=int(row[4]),
                p10_14=int(row[5]),
                p15_19=int(row[6]),
                p20_24=int(row[7]),
                p25_29=int(row[8]),
                p30_34=int(row[9]),
                p35_39=int(row[10]),
                p40_44=int(row[11]),
                p45_49=int(row[12]),
                p50_54=int(row[13]),
                p55_59=int(row[14]),
                p60_64=int(row[15]),
                p65_69=int(row[16]),
                p70_74=int(row[17]),
                p75_79=int(row[18]),
                p80_84=int(row[19]),
                p85=int(row[20])
            )
            db.add(zgony)

        db.commit()
