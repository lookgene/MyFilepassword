from sqlalchemy.orm import Session
from app.models.payment import Payment, PaymentStatus
from app.schemas.payment import PaymentCreate

def get_payment_by_id(db: Session, payment_id: int):
    """通过ID获取支付记录"""
    return db.query(Payment).filter(Payment.id == payment_id).first()

def get_payments_by_user_id(db: Session, user_id: int, skip: int = 0, limit: int = 100):
    """获取用户的所有支付记录"""
    return db.query(Payment).filter(Payment.user_id == user_id).offset(skip).limit(limit).all()

def get_payments_by_task_id(db: Session, task_id: int):
    """获取任务的所有支付记录"""
    return db.query(Payment).filter(Payment.task_id == task_id).all()

def create_payment(db: Session, payment: PaymentCreate):
    """创建新支付记录"""
    db_payment = Payment(
        user_id=payment.user_id,
        task_id=payment.task_id,
        amount=payment.amount,
        payment_method=payment.payment_method,
        status=PaymentStatus.PENDING
    )
    db.add(db_payment)
    db.commit()
    db.refresh(db_payment)
    return db_payment

def update_payment_status(db: Session, payment_id: int, status: PaymentStatus, transaction_id: str = None):
    """更新支付状态"""
    db_payment = db.query(Payment).filter(Payment.id == payment_id).first()
    if db_payment:
        db_payment.status = status
        if transaction_id:
            db_payment.transaction_id = transaction_id
        db.commit()
        db.refresh(db_payment)
        return db_payment
    return None
