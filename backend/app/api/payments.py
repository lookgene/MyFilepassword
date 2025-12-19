from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.payment import PaymentCreate, Payment, PaymentResponse
from app.crud.payment import create_payment, get_payment_by_id, get_payments_by_user_id

router = APIRouter()

@router.post("/create", response_model=PaymentResponse)
def create_payment_record(
    payment: PaymentCreate,
    db: Session = Depends(get_db)
):
    """创建支付记录"""
    db_payment = create_payment(db=db, payment=payment)
    
    return PaymentResponse(
        id=db_payment.id,
        task_id=db_payment.task_id,
        amount=db_payment.amount,
        status=db_payment.status,
        created_at=db_payment.created_at
    )

@router.get("/{payment_id}", response_model=Payment)
def get_payment(payment_id: int, db: Session = Depends(get_db)):
    """获取支付信息"""
    db_payment = get_payment_by_id(db, payment_id=payment_id)
    if db_payment is None:
        raise HTTPException(status_code=404, detail="支付记录未找到")
    return db_payment

@router.get("/user/{user_id}", response_model=list[Payment])
def get_user_payments(user_id: int, db: Session = Depends(get_db)):
    """获取用户的所有支付记录"""
    return get_payments_by_user_id(db, user_id=user_id)
