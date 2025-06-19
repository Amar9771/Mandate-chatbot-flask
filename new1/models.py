from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class Company(Base):
    __tablename__ = 'companies'
    id = Column(Integer, primary_key=True)
    CompanyName = Column(String(200), unique=True)
    Address = Column(Text)
    Email = Column(String(100))
    Phone = Column(String(50))
    Brief = Column(Text)

class BDActivity(Base):
    __tablename__ = 'bdactivities'
    id = Column(Integer, primary_key=True)
    CompanyName = Column(String(200))
    BDName = Column(String(100))
    PersonMet = Column(String(100))
    Minutes = Column(Text)
    EntryDate = Column(DateTime, default=datetime.utcnow)

class BWRClientData(Base):
    __tablename__ = 'bwrclientdata'
    id = Column(Integer, primary_key=True)
    CompanyName = Column(String(200))
    Escalation = Column(Text)
    Alerts = Column(Text)
    Issues = Column(Text)
    RationaleLink = Column(String(500))
    WDRequests = Column(Text)
    RatingHistory = Column(Text)
