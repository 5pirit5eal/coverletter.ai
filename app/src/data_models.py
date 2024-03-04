from sqlalchemy import ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, relationship
from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean


class User(DeclarativeBase):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    fullname = Column(String)
    password = Column(String)
    addresses = relationship("Address", back_populates="user")


if __name__ == '__main__':
    from sqlalchemy import create_engine
    engine = create_engine('sqlite+pysqlite:///:memory:')
    