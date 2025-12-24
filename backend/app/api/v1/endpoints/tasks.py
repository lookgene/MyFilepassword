"""Task endpoints."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.deps import get_current_active_user
from app.db.session import get_db
from app.models.user import User
from app.schemas.common import success_response, PaginationParams
from app.schemas.task import TaskCreate, TaskUpdate, TaskResponse
from app.services.task_service import TaskService

router = APIRouter()


@router.post("", response_model=dict)
async def create_task(
    task_data: TaskCreate,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
):
    """Create a new task.

    Args:
        task_data: Task creation data
        current_user: Current authenticated user
        db: Database session

    Returns:
        Created task information
    """
    task_service = TaskService(db)
    task = await task_service.create_task(current_user.id, task_data)

    return success_response(data=task, message="任务创建成功")


@router.get("", response_model=dict)
async def list_tasks(
    pagination: PaginationParams = Depends(),
    status: str | None = None,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
):
    """List user's tasks.

    Args:
        pagination: Pagination parameters
        status: Filter by status
        current_user: Current authenticated user
        db: Database session

    Returns:
        List of tasks
    """
    task_service = TaskService(db)
    tasks = await task_service.list_tasks(current_user.id, pagination, status)

    return success_response(data=tasks)


@router.get("/{task_id}", response_model=dict)
async def get_task(
    task_id: str,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
):
    """Get task information.

    Args:
        task_id: Task ID
        current_user: Current authenticated user
        db: Database session

    Returns:
        Task information
    """
    task_service = TaskService(db)
    task = await task_service.get_task(task_id, current_user.id)

    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found",
        )

    return success_response(data=task)


@router.patch("/{task_id}", response_model=dict)
async def update_task(
    task_id: str,
    task_data: TaskUpdate,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
):
    """Update task.

    Args:
        task_id: Task ID
        task_data: Task update data
        current_user: Current authenticated user
        db: Database session

    Returns:
        Updated task information
    """
    task_service = TaskService(db)
    task = await task_service.update_task(task_id, current_user.id, task_data)

    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found",
        )

    return success_response(data=task, message="任务已更新")


@router.post("/{task_id}/cancel", response_model=dict)
async def cancel_task(
    task_id: str,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
):
    """Cancel task.

    Args:
        task_id: Task ID
        current_user: Current authenticated user
        db: Database session

    Returns:
        Success message
    """
    task_service = TaskService(db)
    success = await task_service.cancel_task(task_id, current_user.id)

    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found",
        )

    return success_response(message="任务已取消")


@router.get("/{task_id}/progress-stream")
async def task_progress_stream(
    task_id: str,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
):
    """Stream task progress (SSE).

    Args:
        task_id: Task ID
        current_user: Current authenticated user
        db: Database session

    Returns:
        Server-Sent Events stream
    """
    # TODO: Implement SSE streaming
    pass
