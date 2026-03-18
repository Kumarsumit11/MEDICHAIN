from fastapi import APIRouter, HTTPException
from models.user import UserCreate, UserLogin, UserResponse
from utils.security import hash_password, verify_password, generate_user_id, calculate_age, generate_health_id
from database.database import get_db_connection
import datetime

router = APIRouter(prefix="/api/auth", tags=["authentication"])

@router.post("/register")
async def register(user: UserCreate):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Check if user exists
    cursor.execute("SELECT id FROM users WHERE phone = ?", (user.phone,))
    if cursor.fetchone():
        conn.close()
        raise HTTPException(status_code=400, detail="Phone number already registered")
    
    # Create user
    user_id = generate_user_id()
    password_hash = hash_password(user.password)
    current_time = datetime.datetime.now().isoformat()
    health_id = generate_health_id(user_id)
    
    cursor.execute('''
    INSERT INTO users (id, first_name, last_name, phone, emergency_contact, 
                       address, allergies, chronic_diseases, blood_type, 
                       date_of_birth, password_hash, created_at)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        user_id, user.first_name, user.last_name, user.phone, 
        user.emergency_contact, user.address, user.allergies, 
        user.chronic_diseases, user.blood_type, user.date_of_birth, 
        password_hash, current_time
    ))
    
    conn.commit()
    conn.close()
    
    return {
        "success": True,
        "message": "Registration successful",
        "user_id": user_id,
        "health_id": health_id,
        "user": {
            "first_name": user.first_name,
            "last_name": user.last_name,
            "full_name": f"{user.first_name} {user.last_name}",
            "phone": user.phone,
            "blood_type": user.blood_type
        }
    }

@router.post("/login")
async def login(login_data: UserLogin):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
    SELECT id, first_name, last_name, phone, emergency_contact, address, 
           allergies, chronic_diseases, blood_type, date_of_birth, password_hash
    FROM users WHERE phone = ?
    ''', (login_data.phone,))
    
    user_data = cursor.fetchone()
    
    if not user_data:
        conn.close()
        raise HTTPException(status_code=401, detail="Invalid phone or password")
    
    user_id, first_name, last_name, phone, emergency_contact, address, \
    allergies, chronic_diseases, blood_type, date_of_birth, password_hash = user_data
    
    if not verify_password(login_data.password, password_hash):
        conn.close()
        raise HTTPException(status_code=401, detail="Invalid phone or password")
    
    # Update last login time
    current_time = datetime.datetime.now().isoformat()
    cursor.execute("UPDATE users SET last_login = ? WHERE id = ?", (current_time, user_id))
    conn.commit()
    conn.close()
    
    # Calculate age
    age = calculate_age(date_of_birth)
    health_id = generate_health_id(user_id)
    
    return {
        "success": True,
        "message": "Login successful",
        "user_id": user_id,
        "health_id": health_id,
        "user": {
            "id": user_id,
            "first_name": first_name,
            "last_name": last_name,
            "full_name": f"{first_name} {last_name}",
            "phone": phone,
            "emergency_contact": emergency_contact,
            "address": address,
            "allergies": allergies,
            "chronic_diseases": chronic_diseases,
            "blood_type": blood_type,
            "date_of_birth": date_of_birth,
            "age": age,
            "health_id": health_id
        }
    }