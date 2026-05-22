import asyncio
from app.db.session import engine
from app.db.base import Base
# Import all models so SQLAlchemy knows about them before creating tables
from app.models import Role, RoleHierarchy, ModuleAccess, EntityPermission, FieldPermission, RecordAssignment

async def create_tables():
    print("Connecting to the database and creating tables...")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("Tables created successfully!")

if __name__ == "__main__":
    asyncio.run(create_tables())
