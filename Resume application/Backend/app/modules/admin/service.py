from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from fastapi import HTTPException, status
import uuid
from app.shared.auth.models import User
from app.shared.emails.models import EmailTemplate
from app.modules.admin import schemas

async def get_all_users(db: AsyncSession) -> list[User]:
    # Candidates are in a separate table, so no need to filter them out here
    result = await db.execute(select(User).order_by(User.created_at.desc()))
    return result.scalars().all()

async def create_user(db: AsyncSession, user_data: schemas.UserCreate) -> User:
    # Check if email exists
    result = await db.execute(select(User).where(User.email == user_data.email))
    if result.scalar_one_or_none():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")
        
    db_user = User(
        email=user_data.email,
        full_name=user_data.full_name,
        role=user_data.role,
        department=user_data.department,
        is_active=True
    )
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user

async def update_user(db: AsyncSession, user_id: uuid.UUID, user_data: schemas.UserUpdate) -> User:
    user = await db.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
        
    if user_data.full_name is not None:
        user.full_name = user_data.full_name
    if user_data.role is not None:
        user.role = user_data.role
    if user_data.department is not None:
        user.department = user_data.department
    if user_data.is_active is not None:
        user.is_active = user_data.is_active
        
    await db.commit()
    await db.refresh(user)
    return user

async def delete_user(db: AsyncSession, user_id: uuid.UUID) -> bool:
    user = await db.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
        
    await db.delete(user)
    await db.commit()
    return True

async def get_all_email_templates(db: AsyncSession) -> list[EmailTemplate]:
    result = await db.execute(select(EmailTemplate).order_by(EmailTemplate.name))
    return result.scalars().all()

async def save_email_template(db: AsyncSession, template_data: schemas.EmailTemplateCreate) -> EmailTemplate:
    result = await db.execute(select(EmailTemplate).where(EmailTemplate.name == template_data.name))
    template = result.scalar_one_or_none()
    
    if template:
        template.subject = template_data.subject
        template.body_html = template_data.body_html
        template.is_active = template_data.is_active
    else:
        template = EmailTemplate(
            name=template_data.name,
            subject=template_data.subject,
            body_html=template_data.body_html,
            is_active=template_data.is_active
        )
        db.add(template)
        
    await db.commit()
    await db.refresh(template)
    return template
