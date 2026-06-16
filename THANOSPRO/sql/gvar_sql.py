from sqlalchemy import Column, String, UnicodeText, select, delete
from . import BASE
import THANOSPRO.sql as sql

class Gvar(BASE):
    __tablename__ = "gvar"
    variable = Column(String, primary_key=True, nullable=False)
    value = Column(UnicodeText, primary_key=True, nullable=False)

    def __init__(self, variable, value):
        self.variable = str(variable)
        self.value = value

# Table creation is handled in init_db()

def gvarstat(variable):
    if sql.SESSION is None: return None
    try:
        stmt = select(Gvar).where(Gvar.variable == str(variable))
        res = sql.SESSION.execute(stmt).scalars().first()
        return res.value if res else None
    except Exception:
        return None
    finally:
        sql.SESSION.remove()

def addgvar(variable, value):
    if sql.SESSION is None: return
    try:
        delgvar(variable)
        adder = Gvar(str(variable), value)
        sql.SESSION.add(adder)
        sql.SESSION.commit()
    except Exception:
        sql.SESSION.rollback()
    finally:
        sql.SESSION.remove()

def delgvar(variable):
    if sql.SESSION is None: return
    try:
        stmt = delete(Gvar).where(Gvar.variable == str(variable))
        sql.SESSION.execute(stmt)
        sql.SESSION.commit()
    except Exception:
        sql.SESSION.rollback()
    finally:
        sql.SESSION.remove()
