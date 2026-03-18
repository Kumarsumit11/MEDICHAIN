from pydantic import BaseModel, validator
from typing import Optional
from datetime import datetime

class UserCreate(BaseModel):
    first_name: str
    last_name: str
    phone: str
    emergency_contact: str
    address: str
    allergies: Optional[str] = ""
    chronic_diseases: Optional[str] = ""
    blood_type: Optional[str] = ""
    date_of_birth: Optional[str] = ""
    password: str
    
    @validator('phone')
    def validate_phone(cls, v):
        if not v.isdigit() or len(v) != 10:
            raise ValueError('Phone number must be 10 digits')
        return v

class UserLogin(BaseModel):
    phone: str
    password: str

class UserResponse(BaseModel):
    id: str
    first_name: str
    last_name: str
    full_name: str
    phone: str
    emergency_contact: str
    address: str
    allergies: str
    chronic_diseases: str
    blood_type: str
    date_of_birth: str
    age: Optional[int]
    health_id: str

class QRData(BaseModel):
    name: str
    health_id: str
    blood_type: str
    emergency_contact: str
    allergies: str
    chronic_diseases: str

class UserUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    emergency_contact: Optional[str] = None
    address: Optional[str] = None
    allergies: Optional[str] = None
    chronic_diseases: Optional[str] = None
    blood_type: Optional[str] = None
    date_of_birth: Optional[str] = None

class MedicalRecordCreate(BaseModel):
    phone: str
    category: str
    filename: str

class MedicineCreate(BaseModel):
    name: str
    dosage: str
    frequency: str
    duration: str
    prescribed_date: Optional[str] = None