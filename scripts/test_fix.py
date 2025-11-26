from src.sessions.session_service import SessionService
import uuid
import json
import os

# Ensure we use the same DB
os.environ["DATABASE_URL"] = "sqlite:///./data/db.sqlite3"

def test_session_persistence():
    service = SessionService()
    sid = str(uuid.uuid4())
    payload = {"topic": "Test Topic"}
    
    print(f"Creating session {sid}...")
    service.create_session(sid, payload)
    
    print("Attempting to retrieve session payload...")
    try:
        retrieved_payload = service.get_session_payload(sid)
        print(f"Retrieved payload: {retrieved_payload}")
        
        if retrieved_payload == payload:
            print("SUCCESS: Session data persisted and retrieved correctly.")
        else:
            print("FAILURE: Payload mismatch.")
            
    except Exception as e:
        print(f"FAILURE: Error retrieving session: {e}")

if __name__ == "__main__":
    test_session_persistence()
