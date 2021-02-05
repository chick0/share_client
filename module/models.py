# -*- coding: utf-8 -*-

from sqlalchemy import func
from sqlalchemy import Column
from sqlalchemy import Integer, String, Text, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class File(Base):
    __tablename__ = "file"

    idx = Column(
        String(8),
        unique=True,
        primary_key=True,
        nullable=False
    )

    filename = Column(
        String(255),
        nullable=False
    )

    upload = Column(
        DateTime,
        default=func.now(),
        nullable=False
    )

    md5 = Column(
        String(32),
        nullable=False
    )

    size = Column(
        Integer,
        nullable=False
    )

    def __init__(self, idx: str, filename: str, md5: str, size: int):
        self.idx = idx
        self.filename = filename
        self.md5 = md5
        self.size = size

    def __repr__(self):
        return f"<File idx={self.idx!r}>"


class Report(Base):
    __tablename__ = "report"

    md5 = Column(
        String(32),
        unique=True,
        primary_key=True,
        nullable=False
    )

    upload = Column(
        DateTime,
        nullable=False,
        default=func.now()
    )

    text = Column(
        Text,
        nullable=False
    )

    ban = Column(
        Boolean,
        nullable=False,
        default=False
    )

    def __init__(self, md5: str, text: str):
        self.md5 = md5
        self.text = text

    def __repr__(self):
        return f"<Report md5={self.md5!r}>"
