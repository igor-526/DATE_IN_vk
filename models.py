from gino import Gino
from sqlalchemy import Column, String, ForeignKey, DateTime, Integer, Date, sql, Float
import sqlalchemy as sa
from typing import List
import config

db = Gino()

class BaseModel(db.Model):
    __abstract__ = True

    def __str__(self):
        model = self.__class__.__name__
        table: sa.Table = sa.inspect(self.__class__)
        primary_key_columns: List[sa.Column] = table.primary_key.columns
        values = {
            column.name: getattr(self, self._column_name_map[column.name])
            for column in primary_key_columns
        }
        values_str = " ".join(f"{name}={value!r}" for name, value in values.items())
        return f"<{model} {values_str}>"



class Profile(BaseModel):
    __tablename__ = "profile"

    id = Column(Integer, primary_key=True)
    phone = Column(String, nullable=True, unique=True)
    vk_id = Column(Integer, nullable=True, unique=True)
    tg_id = Column(Integer, nullable=True, unique=True)
    name = Column(String, nullable=False)
    bdate = Column(Date, nullable=False)
    sex = Column(Integer, nullable=False)
    city = Column(String, nullable=False)
    geo_lat = Column(Float, nullable=False)
    geo_long = Column(Float, nullable=False)
    description = Column(String, nullable=True)
    status = Column(String, nullable=False)

    query: sql.select


class Settings(BaseModel):
    __tablename__ = "settings"

    id = Column(Integer, primary_key=True)
    age_min = Column(Integer, nullable=False)
    age_max = Column(Integer, nullable=False)
    find_m = Column(Integer, nullable=False)
    find_f = Column(Integer, nullable=False)
    purp1 = Column(Integer, nullable=False)
    purp2 = Column(Integer, nullable=False)
    purp3 = Column(Integer, nullable=False)
    purp4 = Column(Integer, nullable=False)
    purp5 = Column(Integer, nullable=False)
    ch_name = Column(DateTime, nullable=True)
    ch_sex = Column(DateTime, nullable=True)
    ch_bdate = Column(DateTime, nullable=True)
    created = Column(Date, nullable=False)
    deactivated = Column(DateTime, nullable=True)
    last_usage = Column(DateTime, nullable=False)
    offer_kilometrage = Column(Integer, nullable=True)
    offer_ofset = Column(Integer, nullable=True)

    query: sql.select


class Images(BaseModel):
    __tablename__ = "images"

    id = Column(Integer, primary_key=True)
    profile = Column(Integer, nullable=False)
    url = Column(String, nullable=False)
    url_vk = Column(String, nullable=True)
    description = Column(String, nullable=False)

    query: sql.select


class Offerlist(BaseModel):
    __tablename__ = "offerlist"

    id = Column(Integer, primary_key=True)
    profile = Column(Integer, nullable=False)
    offer_id = Column(Integer, nullable=False)
    status = Column(String, nullable=False)

    query: sql.select


class Matchlist(BaseModel):
    __tablename__ = "matchlist"

    id = Column(Integer, primary_key=True)
    profile_1 = Column(Integer, nullable=False)
    profile_2 = Column(Integer, nullable=False)

    query: sql.select


class Complaintlist(BaseModel):
    __tablename__ = "complaintlist"

    id = Column(Integer, primary_key=True)
    profile = Column(Integer, nullable=False)
    complain_to = Column(Integer, nullable=True)
    cat = Column(String, nullable=False)
    description = Column(String, nullable=True)
    images = Column(String, nullable=True)
    status = Column(String, nullable=False)
    date = Column(DateTime, nullable=False)

    query: sql.select


async def db_bind():
    await db.set_bind(config.POSTGRES_URI)
    print("Connected to Database")


async def db_reset():
    await db.gino.drop_all()
    await db.gino.create_all()
    print('Reseted')