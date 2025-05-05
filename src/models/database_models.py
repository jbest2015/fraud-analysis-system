from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, ForeignKey, Boolean, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class FraudIncident(Base):
    __tablename__ = 'fraud_incidents'
    
    id = Column(Integer, primary_key=True)
    incident_id = Column(String, unique=True)
    title = Column(String)
    status = Column(String)
    priority = Column(String)
    report_date = Column(DateTime)
    detection_date = Column(DateTime)
    occurrence_date = Column(DateTime)
    resolution_date = Column(DateTime)
    fraud_type = Column(String)
    sub_type = Column(String)
    fraud_vector = Column(JSON)
    ai_involvement = Column(Boolean)
    detection_method = Column(String)
    risk_score = Column(Integer)
    fraud_pattern_id = Column(String)
    
    # Relationships
    transactions = relationship('Transaction', back_populates='incident')
    investigation_notes = relationship('InvestigationNote', back_populates='incident')

class Transaction(Base):
    __tablename__ = 'transactions'
    
    id = Column(Integer, primary_key=True)
    transaction_id = Column(String, unique=True)
    incident_id = Column(Integer, ForeignKey('fraud_incidents.id'))
    transaction_date = Column(DateTime)
    transaction_type = Column(String)
    amount = Column(Float)
    payment_method = Column(String)
    
    # Relationships
    incident = relationship('FraudIncident', back_populates='transactions')

class InvestigationNote(Base):
    __tablename__ = 'investigation_notes'
    
    id = Column(Integer, primary_key=True)
    incident_id = Column(Integer, ForeignKey('fraud_incidents.id'))
    timestamp = Column(DateTime)
    user_id = Column(String)
    note = Column(String)
    
    # Relationships
    incident = relationship('FraudIncident', back_populates='investigation_notes')