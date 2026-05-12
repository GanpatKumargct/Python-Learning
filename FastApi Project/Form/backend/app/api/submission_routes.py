from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List
from uuid import UUID

from app.db.database import get_db
from app.models.form_model import Form
from app.models.submission_model import FormSubmission
from app.schemas.submission_schema import SubmissionCreate, SubmissionResponse

router = APIRouter(tags=["submissions"])

@router.post("/forms/{form_id}/submit", response_model=SubmissionResponse, status_code=status.HTTP_201_CREATED)
async def submit_form(form_id: UUID, submission: SubmissionCreate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Form).where(Form.id == form_id))
    form = result.scalars().first()
    if not form:
        raise HTTPException(status_code=404, detail="Form not found")
    
    new_submission = FormSubmission(form_id=form_id, **submission.model_dump())
    db.add(new_submission)
    await db.commit()
    await db.refresh(new_submission)
    return new_submission

@router.get("/forms/{form_id}/submissions", response_model=List[SubmissionResponse])
async def get_form_submissions(form_id: UUID, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(FormSubmission).where(FormSubmission.form_id == form_id))
    return result.scalars().all()

@router.get("/submissions/{submission_id}", response_model=SubmissionResponse)
async def get_submission(submission_id: UUID, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(FormSubmission).where(FormSubmission.id == submission_id))
    submission = result.scalars().first()
    if not submission:
        raise HTTPException(status_code=404, detail="Submission not found")
    return submission
