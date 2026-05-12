from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import delete
from typing import List
from uuid import UUID

from app.db.database import get_db
from app.models.form_model import Form
from app.schemas.form_schema import FormCreate, FormUpdate, FormResponse

router = APIRouter(prefix="/forms", tags=["forms"])

@router.post("", response_model=FormResponse, status_code=status.HTTP_201_CREATED)
async def create_form(form: FormCreate, db: AsyncSession = Depends(get_db)):
    new_form = Form(**form.model_dump())
    db.add(new_form)
    await db.commit()
    await db.refresh(new_form)
    return new_form

@router.get("", response_model=List[FormResponse])
async def list_forms(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Form))
    return result.scalars().all()

@router.get("/{form_id}", response_model=FormResponse)
async def get_form(form_id: UUID, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Form).where(Form.id == form_id))
    form = result.scalars().first()
    if not form:
        raise HTTPException(status_code=404, detail="Form not found")
    return form

@router.put("/{form_id}", response_model=FormResponse)
async def update_form(form_id: UUID, form_update: FormUpdate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Form).where(Form.id == form_id))
    form = result.scalars().first()
    if not form:
        raise HTTPException(status_code=404, detail="Form not found")
    
    update_data = form_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(form, key, value)
    
    await db.commit()
    await db.refresh(form)
    return form

@router.delete("/{form_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_form(form_id: UUID, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Form).where(Form.id == form_id))
    form = result.scalars().first()
    if not form:
        raise HTTPException(status_code=404, detail="Form not found")
    
    await db.delete(form)
    await db.commit()
