"""Payment endpoints."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.deps import get_current_active_user
from app.db.session import get_db
from app.models.user import User
from app.schemas.common import success_response
from app.schemas.payment import OrderCreate, RefundCreate
from app.services.payment_service import PaymentService

router = APIRouter()


@router.post("/orders", response_model=dict)
async def create_order(
    order_data: OrderCreate,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
):
    """Create a new order.

    Args:
        order_data: Order creation data
        current_user: Current authenticated user
        db: Database session

    Returns:
        Created order information
    """
    payment_service = PaymentService(db)
    order = await payment_service.create_order(current_user.id, order_data)

    return success_response(data=order, message="订单创建成功")


@router.get("/orders/{order_id}", response_model=dict)
async def get_order(
    order_id: str,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
):
    """Get order information.

    Args:
        order_id: Order ID
        current_user: Current authenticated user
        db: Database session

    Returns:
        Order information
    """
    payment_service = PaymentService(db)
    order = await payment_service.get_order(order_id, current_user.id)

    if order is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found",
        )

    return success_response(data=order)


@router.post("/orders/{order_id}/cancel", response_model=dict)
async def cancel_order(
    order_id: str,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
):
    """Cancel order.

    Args:
        order_id: Order ID
        current_user: Current authenticated user
        db: Database session

    Returns:
        Success message
    """
    payment_service = PaymentService(db)
    success = await payment_service.cancel_order(order_id, current_user.id)

    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found",
        )

    return success_response(message="订单已取消")


@router.post("/orders/{order_id}/refund", response_model=dict)
async def create_refund(
    order_id: str,
    refund_data: RefundCreate,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
):
    """Create refund request.

    Args:
        order_id: Order ID
        refund_data: Refund data
        current_user: Current authenticated user
        db: Database session

    Returns:
        Refund information
    """
    payment_service = PaymentService(db)
    refund = await payment_service.create_refund(order_id, current_user.id, refund_data)

    return success_response(data=refund, message="退款申请已提交")


@router.post("/webhook/{provider}")
async def payment_webhook(
    provider: str,
    webhook_data: dict,
    db: AsyncSession = Depends(get_db),
):
    """Handle payment webhook.

    Args:
        provider: Payment provider (wechat/alipay)
        webhook_data: Webhook data
        db: Database session

    Returns:
        Success response
    """
    payment_service = PaymentService(db)
    await payment_service.handle_webhook(provider, webhook_data)

    return success_response(message="OK")
