import asyncio
import os
import sys

# Add the backend root directory to the python path so we can import from app
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.core.database import AsyncSessionLocal
from app.core.security import hash_password
from app.modules.auth.models import User, UserRole

async def seed_admin():
    async with AsyncSessionLocal() as session:
        # Check if admin exists
        result = await session.execute(select(User).where(User.email == "admin@aerospace.com"))
        admin = result.scalar_one_or_none()
        
        if admin:
            print("Admin user already exists. Email: admin@aerospace.com")
            return

        print("Creating admin user...")
        hashed_pw = hash_password("admin123")
        new_admin = User(
            email="admin@aerospace.com",
            full_name="System Administrator",
            password_hash=hashed_pw,
            role=UserRole.admin,
            department="IT"
        )
        
        session.add(new_admin)
        await session.commit()
        print("Admin user created successfully!")
        print("   Email: admin@aerospace.com")
        print("   Password: admin123")

if __name__ == "__main__":
    print("Starting database seed...")
    asyncio.run(seed_admin())
