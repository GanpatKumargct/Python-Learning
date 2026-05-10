import asyncio
import os
import sys

# Add the backend root directory to the python path so we can import from app
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import AsyncSessionLocal
from app.modules.auth.service import authenticate_user, create_tokens_for_user

async def test_login():
    async with AsyncSessionLocal() as session:
        user = await authenticate_user(session, "admin@aerospace.com", "admin123")
        if not user:
            print("Auth failed!")
            return
        print(f"Auth success! User: {user.email}")
        try:
            tokens = await create_tokens_for_user(session, user)
            print(f"Tokens: {tokens}")
        except Exception as e:
            print(f"Error creating tokens: {repr(e)}")
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_login())
