from fastapi import APIRouter, HTTPException, Depends, status, Path, Query
from sqlalchemy.ext.asyncio import AsyncSession
# from asyncpg.exceptions import UniqueViolationError

from src.database.db import get_db
from src.repository import contacts as repositories_contacts
from src.schemas.contact import ContactSchema, ContactUpdateSchema, ContactResponse
from pydantic import ValidationError

router = APIRouter(prefix='/contacts', tags=['contacts'])
search_router = APIRouter(prefix='/search', tags=['search'])

@router.get("/", response_model=list[ContactResponse])
async def get_contacts(limit: int = Query(10, ge=10, le=500), offset: int = Query(0, ge=0),
                    db: AsyncSession = Depends(get_db)):
    contacts = await repositories_contacts.get_contacts(limit, offset, db)
    return contacts

@search_router.get("/name", response_model=list[ContactResponse])
async def get_contacts_by_name(name: str = Query(), db: AsyncSession = Depends(get_db)):
    contacts = await repositories_contacts.get_contacts_by_name(name, db)
    if contacts is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="NOT FOUND")
    return contacts

@search_router.get("/surname", response_model=list[ContactResponse])
async def get_contacts_by_surname(surname: str = Query(), db: AsyncSession = Depends(get_db)):
    contacts = await repositories_contacts.get_contacts_by_surname(surname, db)
    if contacts is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="NOT FOUND")
    return contacts

@search_router.get("/email", response_model=ContactResponse)
async def get_contact_by_email(email: str = Query(), db: AsyncSession = Depends(get_db)):
    contact = await repositories_contacts.get_contact_by_email(email, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="NOT FOUND")
    return contact


@router.get("/{contact_id}", response_model=ContactResponse)
async def get_contact(contact_id: int = Path(ge=1), db: AsyncSession = Depends(get_db)):
    contact = await repositories_contacts.get_contact(contact_id, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="NOT FOUND")
    return contact


@router.post("/", response_model=ContactResponse, status_code=status.HTTP_201_CREATED)
async def create_contact(body: ContactSchema, db: AsyncSession = Depends(get_db)):
    cont = await repositories_contacts.get_contact_by_email(body.email, db)
    if cont is not None:
            raise HTTPException(status_code=400, detail="Email not unique")
    contact = await repositories_contacts.create_contact(body, db)
    return contact  


@router.put("/{contact_id}")
async def update_contact(body: ContactUpdateSchema, contact_id: int = Path(ge=1), db: AsyncSession = Depends(get_db)):
    cont = await repositories_contacts.get_contact_by_email(body.email, db)
    if cont is not None:
            raise HTTPException(status_code=400, detail="Email not unique")
    contact = await repositories_contacts.update_contact(contact_id, body, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="NOT FOUND")
    return contact


@router.delete("/{contact_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_contact(contact_id: int = Path(ge=1), db: AsyncSession = Depends(get_db)):
    contact = await repositories_contacts.delete_contact(contact_id, db)
    return contact