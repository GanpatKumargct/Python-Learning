import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from fastapi import HTTPException
from app.modules.ats.requisitions.models import HiringRequisition, RequisitionStatus, ApprovalStage, RequisitionApproval, RequisitionSupportingMember
from app.modules.ats.requisitions import schemas

async def create_requisition(db: AsyncSession, data: schemas.RequisitionCreate, user_id: uuid.UUID) -> HiringRequisition:
    new_req = HiringRequisition(
        title=data.title,
        job_description=data.job_description,
        scope_of_work=data.scope_of_work,
        department=data.department,
        status=RequisitionStatus.draft,
        created_by=user_id,
        screening_form_id=data.screening_form_id
    )
    db.add(new_req)
    await db.flush()

    if data.supporting_members:
        for member_id in data.supporting_members:
            db.add(RequisitionSupportingMember(requisition_id=new_req.id, user_id=member_id))
    
    await db.commit()
    await db.refresh(new_req)
    return new_req

async def get_requisitions(db: AsyncSession) -> list[HiringRequisition]:
    result = await db.execute(select(HiringRequisition).order_by(HiringRequisition.created_at.desc()))
    return result.scalars().all()

async def submit_for_approval(db: AsyncSession, req_id: uuid.UUID) -> HiringRequisition:
    req = await db.get(HiringRequisition, req_id)
    if not req:
        raise HTTPException(status_code=404, detail="Requisition not found")
    if req.status != RequisitionStatus.draft:
        raise HTTPException(status_code=400, detail="Only draft requisitions can be submitted")
    
    req.status = RequisitionStatus.pending_director
    
    # Create the first approval stage row
    approval = RequisitionApproval(
        requisition_id=req.id,
        stage=ApprovalStage.director
    )
    db.add(approval)
    await db.commit()
    await db.refresh(req)
    return req
