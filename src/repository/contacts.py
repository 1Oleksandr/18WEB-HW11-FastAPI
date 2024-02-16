import datetime as DT
from sqlalchemy import select, func, extract, and_
from datetime import date, timedelta
# from sqlalchemy.sql.sqltypes import Date
from sqlalchemy.ext.asyncio import AsyncSession


from src.models.models import Contact
from src.schemas.contact import ContactSchema, ContactUpdateSchema

    
async def get_contacts(limit: int, offset: int, db: AsyncSession):
    stmt = select(Contact).offset(offset).limit(limit)
    contacts = await db.execute(stmt)
    return contacts.scalars().all()


async def get_contact(contact_id: int, db: AsyncSession):
    stmt = select(Contact).filter_by(id=contact_id)
    contact = await db.execute(stmt)
    return contact.scalar_one_or_none()

async def get_contacts_by_name(contact_name: str, db: AsyncSession):
    stmt = select(Contact).where(Contact.name.ilike(contact_name))
    # stmt = select(Contact).filter_by(name = contact_name)
    contacts = await db.execute(stmt)
    return contacts.scalars().all()

async def get_contacts_by_surname(contact_surname: str, db: AsyncSession):
    stmt = select(Contact).where(Contact.surname.ilike(contact_surname))
    # stmt = select(Contact).filter_by(surname = contact_surname)
    contacts = await db.execute(stmt)
    return contacts.scalars().all()

async def get_contact_by_email(contact_email: str, db: AsyncSession):
    stmt = select(Contact).filter_by(email = contact_email)
    contact = await db.execute(stmt)
    return contact.scalar_one_or_none()

async def get_contact_by_birthday(birthday: date, n:int, db: AsyncSession):
    # today = date.today()
    seven_days_later = birthday+ timedelta(days=n)
    stmt = select(Contact).where(and_(Contact.birthday != None, Contact.b_date.between(birthday, seven_days_later)))
    contacts = await db.execute(stmt)
    return contacts.scalars().all()

async def create_contact(body: ContactSchema, db: AsyncSession):
    contact = Contact(**body.model_dump(exclude_unset=True))
    db.add(contact)
    await db.commit()
    await db.refresh(contact)
    return contact


async def update_contact(contact_id: int, body: ContactUpdateSchema, db: AsyncSession):
    stmt = select(Contact).filter_by(id=contact_id)
    result = await db.execute(stmt)
    contact = result.scalar_one_or_none()
    if contact:
        contact.name = body.name
        contact.surname = body.surname
        contact.email = body.email
        contact.birthday = body.birthday
        contact.phone = body.phone
        contact.info = body.info
        contact.created_at = func.now()
        await db.commit()
        await db.refresh(contact)
    return contact


async def delete_contact(contact_id: int, db: AsyncSession):
    stmt = select(Contact).filter_by(id=contact_id)
    contact = await db.execute(stmt)
    contact = contact.scalar_one_or_none()
    if contact:
        await db.delete(contact)
        await db.commit()
    return contact