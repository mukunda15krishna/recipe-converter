from database import SessionLocal
from models import NoteRequest

db = SessionLocal()

request = NoteRequest(
    recipe_id=1,
    request_type="EDIT",
    note_content="""
Reduce water by 3%
during rainy season.aava Mukunda 
""",
    status="PENDING",
    created_at="2026-08-09 10:00 AM"
)

db.add(request)

db.commit()

db.close()

print("Test request created!")