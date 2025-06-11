from sqlalchemy import Column, Integer, String
from Demografia.Database import Base


class Demografia(Base):
    __tablename__ = "ludnosc_woj"

    id = Column(Integer, primary_key=True, index=True)
    wojewodztwa = Column(String)
    rok = Column(Integer)
    liczba_ludnosci = Column(Integer)
    kobiety = Column(Integer)
    mezczyzni = Column(Integer)

    def __init__(self, wojewodztwa, rok, liczba_ludnosci, kobiety, mezczyzni):
        self.wojewodztwa = wojewodztwa
        self.rok = rok
        self.liczba_ludnosci = liczba_ludnosci
        self.kobiety = kobiety
        self.mezczyzni = mezczyzni


class Zgony(Base):
    __tablename__ = "zgony_woj"

    id = Column(Integer, primary_key=True, index=True)
    wojewodztwa = Column(String)
    rok = Column(Integer)
    liczba_ogolem = Column(Integer)
    p0_4 = Column(Integer)
    p5_9 = Column(Integer)
    p10_14 = Column(Integer)
    p15_19 = Column(Integer)
    p20_24 = Column(Integer)
    p25_29 = Column(Integer)
    p30_34 = Column(Integer)
    p35_39 = Column(Integer)
    p40_44 = Column(Integer)
    p45_49 = Column(Integer)
    p50_54 = Column(Integer)
    p55_59 = Column(Integer)
    p60_64 = Column(Integer)
    p65_69 = Column(Integer)
    p70_74 = Column(Integer)
    p75_79 = Column(Integer)
    p80_84 = Column(Integer)
    p85 = Column(Integer)

    def __init__(self, wojewodztwa, rok, liczba_ogolem, p0_4, p5_9, p10_14, p15_19, p20_24, p25_29, p30_34,
                 p35_39, p40_44, p45_49, p50_54, p55_59, p60_64, p65_69, p70_74, p75_79, p80_84, p85):
        self.wojewodztwa = wojewodztwa
        self.rok = rok
        self.liczba_ogolem = liczba_ogolem
        self.p0_4 = p0_4
        self.p5_9 = p5_9
        self.p10_14 = p10_14
        self.p15_19 = p15_19
        self.p20_24 = p20_24
        self.p25_29 = p25_29
        self.p30_34 = p30_34
        self.p35_39 = p35_39
        self.p40_44 = p40_44
        self.p45_49 = p45_49
        self.p50_54 = p50_54
        self.p55_59 = p55_59
        self.p60_64 = p60_64
        self.p65_69 = p65_69
        self.p70_74 = p70_74
        self.p75_79 = p75_79
        self.p80_84 = p80_84
        self.p85 = p85

class Urodzenia(Base):
    __tablename__ = "urodzenia_woj"

    id = Column(Integer, primary_key=True, index=True)
    wojewodztwa = Column(String)
    rok = Column(Integer)
    liczba_ogolem = Column(Integer)
    chlopcy = Column(Integer)
    dzieczeta = Column(Integer)