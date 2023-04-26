from gino import Gino
from sqlalchemy import Column, BigInteger, String, ForeignKey, DateTime, Integer, Float, Date, Boolean, sql
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
    vk_id = Column(Integer, nullable=True)
    tg_id = Column(Integer, nullable=True)
    name = Column(String, nullable=False)
    age = Column(Integer, nullable=False)
    sex = Column(Integer, nullable=False)
    city_id = Column(Integer, nullable=False)
    city_title = Column(String, nullable=False)
    description = Column(String, nullable=True)
    age_min = Column(Integer, nullable=False)
    age_max = Column(Integer, nullable=False)
    find_m = Column(Integer, nullable=False)
    find_f = Column(Integer, nullable=False)
    purp1 = Column(Integer, nullable=False)
    purp2 = Column(Integer, nullable=False)
    purp3 = Column(Integer, nullable=False)
    purp4 = Column(Integer, nullable=False)
    purp5 = Column(Integer, nullable=False)

    query: sql.select


class Images(BaseModel):
    __tablename__ = "images"

    id = Column(Integer, primary_key=True)
    profile = Column(Integer, nullable=False)
    url = Column(String, nullable=False)
    description = Column(String, nullable=False)

    query: sql.select


async def db_bind():
    await db.set_bind(config.POSTGRES_URI)
    print("Connected to Database")


async def db_reset():
    await db.gino.drop_all()
    await db.gino.create_all()
    print('Reseted')