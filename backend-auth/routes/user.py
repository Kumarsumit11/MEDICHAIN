from fastapi import APIRouter, HTTPException
from models.user import UserResponse, UserUpdate, QRData
from utils.security import calculate_age, generate_health_id
from database.database import get_db_connection

router = APIRouter(prefix="/api/user", tags=["user"])

@router.get("/{phone}", response_model=UserResponse)
async def get_user(phone: str):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
    SELECT id, first_name, last_name, phone, emergency_contact, address, 
           allergies, chronic_diseases, blood_type, date_of_birth
    FROM users WHERE phone = ?
    ''', (phone,))
    
    user_data = cursor.fetchone()
    conn.close()
    
    if not user_data:
        raise HTTPException(status_code=404, detail="User not found")
    
    user_id, first_name, last_name, phone, emergency_contact, address, \
    allergies, chronic_diseases, blood_type, date_of_birth = user_data
    
    age = calculate_age(date_of_birth)
    health_id = generate_health_id(user_id)
    
    return UserResponse(
        id=user_id,
        first_name=first_name,
        last_name=last_name,
        full_name=f"{first_name} {last_name}",
        phone=phone,
        emergency_contact=emergency_contact,
        address=address,
        allergies=allergies,
        chronic_diseases=chronic_diseases,
        blood_type=blood_type,
        date_of_birth=date_of_birth,
        age=age,
        health_id=health_id
    )

@router.get("/qr/{phone}", response_model=QRData)
async def get_qr_data(phone: str):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
    SELECT first_name, last_name, blood_type, emergency_contact, allergies, chronic_diseases
    FROM users WHERE phone = ?
    ''', (phone,))
    
    user_data = cursor.fetchone()
    conn.close()
    
    if not user_data:
        raise HTTPException(status_code=404, detail="User not found")
    
    first_name, last_name, blood_type, emergency_contact, allergies, chronic_diseases = user_data
    
    # Get user ID for health ID
    cursor.execute("SELECT id FROM users WHERE phone = ?", (phone,))
    user_id = cursor.fetchone()["id"]
    health_id = generate_health_id(user_id)
    
    return QRData(
        name=f"{first_name} {last_name}",
        health_id=health_id,
        blood_type=blood_type,
        emergency_contact=emergency_contact,
        allergies=allergies,
        chronic_diseases=chronic_diseases
    )

@router.put("/{phone}")
async def update_user(phone: str, user_update: UserUpdate):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Check if user exists
    cursor.execute("SELECT id FROM users WHERE phone = ?", (phone,))
    if not cursor.fetchone():
        conn.close()
        raise HTTPException(status_code=404, detail="User not found")
    
    # Build update query
    update_data = user_update.dict(exclude_unset=True)
    if not update_data:
        conn.close()
        raise HTTPException(status_code=400, detail="No fields to update")
    
    set_clause = ", ".join([f"{key} = ?" for key in update_data.keys()])
    values = list(update_data.values())
    values.append(phone)
    
    cursor.execute(f"UPDATE users SET {set_clause} WHERE phone = ?", values)
    conn.commit()
    conn.close()
    
    return {"success": True, "message": "User updated successfully"}