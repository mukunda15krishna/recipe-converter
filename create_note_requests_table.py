from database import engine
from models import NoteRequest

NoteRequest.__table__.create(
    bind=engine,
    checkfirst=True
)

print("note_requests table created successfully!")