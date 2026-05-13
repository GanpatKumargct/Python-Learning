import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from app.shared.forms.models import Form, FormField
from app.shared.forms import schemas

async def create_dynamic_table(db: AsyncSession, table_name: str, fields: list[schemas.FormFieldCreate]):
    """
    Executes raw DDL to create a dynamic table for storing form responses.
    """
    columns = [
        "id UUID PRIMARY KEY DEFAULT gen_random_uuid()",
        "candidate_id UUID REFERENCES candidates(id) ON DELETE SET NULL",
        "submitted_at TIMESTAMPTZ DEFAULT NOW()"
    ]
    
    for field in fields:
        # Sanitize column name (basic)
        col_name = "".join(c for c in field.field_key if c.isalnum() or c == '_')
        col_type = field.column_type or "TEXT"
        nullable = "NOT NULL" if field.is_required else ""
        columns.append(f"{col_name} {col_type} {nullable}")
        
    create_stmt = f"CREATE TABLE {table_name} ({', '.join(columns)});"
    await db.execute(text(create_stmt))


async def create_form(db: AsyncSession, form_data: schemas.FormCreate, user_id: uuid.UUID) -> Form:
    # 1. Generate unique table name
    form_id = uuid.uuid4()
    # Format: resp_ats_1234abcd
    table_name = f"resp_{form_data.module}_{form_id.hex[:8]}"
    
    # 2. Create the physical PostgreSQL table using DDL
    await create_dynamic_table(db, table_name, form_data.fields)
    
    # 3. Store form metadata
    db_form = Form(
        id=form_id,
        title=form_data.title,
        description=form_data.description,
        department=form_data.department,
        module=form_data.module,
        response_table=table_name,
        created_by=user_id
    )
    db.add(db_form)
    
    # 4. Store field metadata
    for field in form_data.fields:
        db_field = FormField(
            form_id=form_id,
            field_key=field.field_key,
            label=field.label,
            field_type=field.field_type,
            is_required=field.is_required,
            options=field.options,
            validation=field.validation,
            display_order=field.display_order,
            column_type=field.column_type
        )
        db.add(db_field)
        
    await db.commit()
    await db.refresh(db_form)
    
    # Fetch with fields loaded for response
    result = await db.execute(
        select(Form)
        .options(selectinload(Form.fields))
        .where(Form.id == form_id)
    )
    return result.scalar_one()

async def get_forms(db: AsyncSession) -> list[Form]:
    result = await db.execute(select(Form).order_by(Form.created_at.desc()))
    return result.scalars().all()

async def get_form_by_id(db: AsyncSession, form_id: uuid.UUID) -> Form | None:
    result = await db.execute(
        select(Form)
        .options(selectinload(Form.fields))
        .where(Form.id == form_id)
    )
    return result.scalar_one_or_none()
