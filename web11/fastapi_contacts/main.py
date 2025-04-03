from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal, engine, Base
import crud
import schemas

app = FastAPI(title="Contacts API")

Base.metadata.create_all(bind=engine)

# Функція отримання сесії БД
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/contacts/", response_model=schemas.ContactResponse)
def create_contact(contact: schemas.ContactCreate, db: Session = Depends(get_db)):
    return crud.create_contact(db, contact)

@app.get("/contacts/", response_model=list[schemas.ContactResponse])
def get_contacts(db: Session = Depends(get_db)):
    return crud.get_contacts(db)

@app.get("/contacts/{contact_id}", response_model=schemas.ContactResponse)
def get_contact(contact_id: int, db: Session = Depends(get_db)):
    contact = crud.get_contact(db, contact_id)
    if not contact:
        raise HTTPException(status_code=404, detail="Contact not found")
    return contact

@app.put("/contacts/{contact_id}", response_model=schemas.ContactResponse)
def update_contact(contact_id: int, contact: schemas.ContactCreate, db: Session = Depends(get_db)):
    updated_contact = crud.update_contact(db, contact_id, contact)
    if not updated_contact:
        raise HTTPException(status_code=404, detail="Contact not found")
    return updated_contact

@app.delete("/contacts/{contact_id}")
def delete_contact(contact_id: int, db: Session = Depends(get_db)):
    deleted_contact = crud.delete_contact(db, contact_id)
    if not deleted_contact:
        raise HTTPException(status_code=404, detail="Contact not found")
    return {"message": "Contact deleted successfully"}

@app.get("/contacts/search/")
def search_contacts(query: str, db: Session = Depends(get_db)):
    return crud.search_contacts(db, query)

@app.get("/contacts/birthdays/")
def get_upcoming_birthdays(db: Session = Depends(get_db)):
    return crud.upcoming_birthdays(db)
