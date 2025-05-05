import sys
from pathlib import Path
from database.db_manager import DatabaseManager
from utils.data_parser import parse_json_file, parse_incident

def main():
    # Initialize database
    db = DatabaseManager()
    db.init_db()
    
    # Get the data file path
    data_file = Path("testdata.txt")
    if not data_file.exists():
        print(f"Error: Could not find data file at {data_file}")
        sys.exit(1)
    
    try:
        # Parse incidents from JSON file
        incidents_data = parse_json_file(data_file)
        
        # Get database session
        session = db.get_session()
        
        # Process each incident
        for incident_data in incidents_data:
            try:
                # Parse and create incident with related objects
                incident = parse_incident(incident_data)
                
                # Add to session
                session.add(incident)
                
            except Exception as e:
                print(f"Error processing incident {incident_data.get('incident_id')}: {str(e)}")
                continue
        
        # Commit all changes
        session.commit()
        print("Successfully imported all incidents")
        
    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1)
    
    finally:
        session.close()
        db.close()

if __name__ == "__main__":
    main()