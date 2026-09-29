from fastapi import FastAPI, Depends
from pydantic import BaseModel, EmailStr
from sqlalchemy import create_engine, Column, Integer, String, Text
from sqlalchemy.orm import declarative_base, Session
from app.database import get_db, engine


app = FastAPI()

Base = declarative_base()

class Contact(Base):
    __tablename__ = "contacts"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(250), nullable=False)
    message = Column(Text, nullable=False)

Base.metadata.create_all(bind=engine)

class ContactRequest(BaseModel):
    name: str
    email: EmailStr
    message: str



@app.post("/contact")
def create_contact(contact: ContactRequest, db: Session=Depends(get_db)):
    new_contact = Contact(
        name=contact.name,
        email=contact.email,
        message=contact.message
    )

    db.add(new_contact)
    db.commit()
    db.refresh(new_contact)

    return {
        "message": "Contact us submitted succesfully",
        "id": new_contact.id
    }

    
@app.get("/")
def root():
    return {"message": "DifferentByte Machine Test API"}
