import json
from datetime import datetime
from typing import Dict, Any, List
from ..models.database_models import (
    FraudIncident, Transaction, InvestigationNote
)

def parse_datetime(date_str: str) -> datetime:
    """Parse datetime string to datetime object"""
    if not date_str:
        return None
    return datetime.fromisoformat(date_str.replace('Z', '+00:00'))

def parse_incident(incident_data: Dict[str, Any]) -> Dict[str, Any]:
    """Parse incident data and create database objects"""
    
    # Create main incident object
    incident = FraudIncident(
        incident_id=incident_data['incident_id'],
        title=incident_data['title'],
        status=incident_data['status'],
        priority=incident_data['priority'],
        report_date=parse_datetime(incident_data.get('report_date')),
        detection_date=parse_datetime(incident_data.get('detection_date')),
        occurrence_date=parse_datetime(incident_data.get('occurrence_date')),
        resolution_date=parse_datetime(incident_data.get('resolution_date')),
        fraud_type=incident_data.get('fraud_type'),
        sub_type=incident_data.get('sub_type'),
        fraud_vector=incident_data.get('fraud_vector'),
        ai_involvement=incident_data.get('ai_involvement', False),
        detection_method=incident_data.get('detection_method'),
        risk_score=incident_data.get('risk_score'),
        fraud_pattern_id=incident_data.get('fraud_pattern_id')
    )
    
    return incident

def parse_json_file(file_path: str) -> List[Dict[str, Any]]:
    """Parse JSON file and return list of incidents"""
    with open(file_path, 'r') as f:
        return json.load(f)