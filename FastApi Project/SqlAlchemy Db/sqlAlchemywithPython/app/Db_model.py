
from sqlalchemy import Column, Integer, String,Float
from sqlalchemy.sql.sqltypes import TIMESTAMP # type: ignore
from sqlalchemy.sql.expression import text    #type:ignore
from .database import Base


class Product(Base):
    __tablename__ = "Product"

    id = Column(Integer, primary_key=True, nullable=False, index=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=False)
    price = Column(Float,  nullable = False)
    quantity = Column(Integer)
    



