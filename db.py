#!/usr/bin/python3
"""‘p1user1’, ‘p1user2’, …, ‘p2user1’"""
from string import hexdigits
from typing import Optional

from sqlalchemy import create_engine  # type: ignore
from sqlalchemy import Column, Integer, String, DateTime  # type: ignore
from sqlalchemy import UniqueConstraint, ForeignKey, func  # type: ignore
from sqlalchemy.ext.declarative import declarative_base  # type: ignore
from sqlalchemy.orm import sessionmaker  # type: ignore

from config import debug, db_url

Base = declarative_base()
engine = create_engine(db_url, echo=debug)
Session = sessionmaker(bind=engine)


class Group(Base):  # type: ignore
    __tablename__ = "group"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=True)
    description = Column(String, nullable=False, unique=True)


class User(Base):  # type: ignore
    __tablename__ = "user"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    password = Column(String, nullable=False)
    group_id = Column(Integer, ForeignKey("group.id"), nullable=False)
    date = Column(DateTime, default=None)
    owner = Column(String, default=None)


def init_db():
    from random import choices
    from string import ascii_letters as letters, hexdigits

    groups = [
        {"id": 1, "description": "Ancient Greek Drama"},
        {"id": 2, "description": "Scientific Revolution"},
        {"id": 3, "description": "Fairy Tales"},
    ]

    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()

    session.add_all(
        Group(id=g["id"], name=f'pilot{g["id"]}', description=g["description"])
        for g in groups
    )

    for g in groups:
        for n in range(1, 9):
            session.add(
                User(
                    id=10 * g["id"] + n,
                    name=f"pilot.{g['id']}.vast+user{n}@gmail.com",
                    password=f"V@stP1lot{g['id']}",
                    group_id=g["id"],
                )
            )

    session.commit()


if __name__ == "__main__":
    init_db()
