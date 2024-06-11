from typing import List

from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session

from ..database.db import get_db
from ..schemas import ContactModel, ContactResponse
from  ..repository import notes as repository_notes


router = APIRouter(prefix='/contacts', tags=["contacts"])


@router.get("/search", response_model=ContactResponse|List[ContactResponse])
async def find_contacts(query: str,  db: Session = Depends(get_db)):
    contacts = await repository_notes.find_name(query, db)
    if  contacts is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")
    return contacts

@router.get("/email", response_model=ContactResponse|List[ContactResponse])
async def find_contacts(contact_email:str,  db: Session = Depends(get_db)):
    contacts = await repository_notes.find_email(contact_email, db)
    if  contacts is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")
    return contacts

@router.get("/upcoming", response_model=ContactResponse|List[ContactResponse])
async def upcoming_birthdays_contacts(skip: int = None, limit: int = None, db: Session = Depends(get_db)):
    contacts = await repository_notes.get_upcoming_birthdays(skip, limit, db)
    if  contacts is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")
    return contacts

@router.get("/", response_model=List[ContactResponse])
async def read_contacts(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    contacts = await repository_notes.get_contacts(skip, limit, db)
    return contacts

@router.get("/{contact_id}", response_model=ContactResponse)
async def read_contact(contact_id: int, db: Session = Depends(get_db)):
    contact = await repository_notes.get_contact(contact_id, db)
    if  contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")
    return contact


@router.post("/", response_model=ContactResponse)
async def create_contact(body: ContactModel, db: Session = Depends(get_db)):
    return await repository_notes.create_contact(body, db)

@router.put("/{contact_id}", response_model=ContactResponse)
async def update_contact(body: ContactModel, contact_id: int, db: Session = Depends(get_db)):
    contact = await repository_notes.update_contact(contact_id, body, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")
    return contact

@router.delete("/{contact_id}", response_model=ContactResponse)
async def remove_contact(contact_id: int, db: Session = Depends(get_db)):
    contact = await repository_notes.remove_contact(contact_id, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")
    return contact




