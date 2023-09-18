from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean, Float
from sqlalchemy.orm import declarative_base, relationship


Base = declarative_base()


class Products(Base):
    __tablename__ = 'un_cg_product'

    markingofthegood = Column(Integer, primary_key=True)
    name = Column(String)
    group_code = Column(String, ForeignKey('un_cg_group.code'))


class Groups(Base):
    __tablename__ = 'un_cg_group'

    code = Column(Integer, primary_key=True)
    parent_code = Column(Integer)
    name = Column(String)
    last_name = Column(String)


class Spirits(Base):
    __tablename__ = 'un_cg_product_spirits'

    status = Column(Integer, primary_key=True)
    markingofthegood = Column(Integer, ForeignKey('un_cg_product.markingofthegood'))
    alcoholic_content = Column(Float)


