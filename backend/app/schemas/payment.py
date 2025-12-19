from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from enum import Enum
from decimal import Decimal

class PaymentStatus(str, Enum):
    PENDING = "pending"
    PAID = "paid"
    REFUNDED = "refunded"
    FAILED = "failed"

class PaymentBase(BaseModel):
    task_id: int
    amount: Decimal
    payment_method: str
    user_id: Optional[int] = None

class PaymentCreate(PaymentBase):
    pass

class Payment(PaymentBase):
    id: int
    status: PaymentStatus
    transaction_id: Optional[str] = None
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class PaymentResponse(BaseModel):
    id: int
    task_id: int
    amount: Decimal
    status: PaymentStatus
    created_at: datetime

    class Config:
        from_attributes = True
