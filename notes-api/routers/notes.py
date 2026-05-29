from fastapi import HTTPException, APIRouter, Depends
from sqlalchemy.orm import Session 
import models, schemas
from database import get_db 

router = APIRouter(
    prefix="/notes",
    tags= ["notes"],
)

@router.post("/", response_model = schemas.NoteResponse)
def create_note(note: schemas.NoteCreate, db: Session = Depends(get_db)):
    db_note = models.Note(title=note.title, content = note.content)
    db.add(db_note)
    db.commit()
    db.refresh(db_note) #now db_note will include the stuff MySQL generates
    return db_note

@router.get("/", response_model = list[schemas.NoteResponse])
def get_notes(db: Session = Depends(get_db)):
    return db.query(models.Note).all() #.all() returns a list instead of a query object

@router.get("/{note_id}", response_model = schemas.NoteResponse)
def get_note(note_id: int, db: Session = Depends(get_db)):
    note = db.query(models.Note).filter(models.Note.id == note_id).first()
    if not note:
        raise HTTPException (status_code=404, detail= f"Note {note_id} not found")
    return note

@router.put("/{note_id}", response_model= schemas.NoteResponse)
def update_note(note_id: int, updated: schemas.NoteUpdate, db: Session = Depends(get_db)):
    note = db.query(models.Note).filter(models.Note.id == note_id).first()
    if not note: 
        raise HTTPException (status_code=404, detail= f"Note {note_id} not found")
    
    if updated.title is not None:
        note.title = updated.title
    if updated.content is not None:
        note.content = updated.content
    db.commit()
    db.refresh(note)
    return note

@router.delete("/{note_id}")
def del_note(note_id: int, db: Session = Depends(get_db)):
    note = db.query(models.Note).first()
    if not note: 
        raise HTTPException (status_code=404, detail= f"Note {note_id} not found")
    db.delete(note)
    db.commit()
    return {"Message":"Deleted Note Successfully"}

