import hashlib
import uuid
from datetime import datetime

def hash_password(password: str) -> str:
    """Hash password using SHA-256"""
    return hashlib.sha256(password.encode()).hexdigest()

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify password against hash"""
    return hash_password(plain_password) == hashed_password

def generate_user_id() -> str:
    """Generate unique user ID"""
    return str(uuid.uuid4())

def calculate_age(dob: str) -> int:
    """Calculate age from date of birth (YYYY-MM-DD format)"""
    if not dob:
        return 0
    try:
        birth_date = datetime.strptime(dob, "%Y-%m-%d")
        today = datetime.now()
        age = today.year - birth_date.year
        if (today.month, today.day) < (birth_date.month, birth_date.day):
            age -= 1
        return age
    except:
        return 0

def generate_health_id(user_id: str) -> str:
    """Generate health ID from user ID and current year"""
    current_year = datetime.now().year
    short_id = user_id[:4].upper()
    return f"MED-{current_year}-{short_id}"