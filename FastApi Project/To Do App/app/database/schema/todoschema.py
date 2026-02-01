from sqlalchemy import column, Integer, String, Boolean, VARCHAR, DateTime

from ..db import Base
from datetime import datetime, timezone

class createtodo(Base):
    __tablename__ = "todos"

    id = column(Integer, primary_key=True, index=True, autoincreament=True)
    content = column(String, nullable=False)
    is_completed = column(Boolean, default=False, nullable=False)
    created_at = column(DateTime, nullable=False, default=datetime.now(timezone.utc))
    updated_at = column(DateTime, nullable=True, default=datetime.now(timezone.utc))