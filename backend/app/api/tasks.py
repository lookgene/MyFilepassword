from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.task import TaskCreate, Task, TaskResponse
from app.crud.task import create_task, get_task_by_id, get_tasks_by_user_id
from app.services.crack import start_crack_task
from app.services.email import email_service

router = APIRouter()

@router.post("/create", response_model=TaskResponse)
def create_crack_task(
    task: TaskCreate,
    db: Session = Depends(get_db)
):
    """创建破解任务"""
    # 创建任务记录
    db_task = create_task(db=db, task=task)
    
    # 发送任务创建通知邮件
    email_service.send_task_created_email(
        email=task.email,
        task_id=db_task.id,
        crack_type=db_task.crack_type
    )
    
    # 启动破解任务
    start_crack_task.delay(db_task.id)
    
    return TaskResponse(
        id=db_task.id,
        file_id=db_task.file_id,
        crack_type=db_task.crack_type,
        status=db_task.status,
        created_at=db_task.created_at,
        estimated_time=db_task.estimated_time
    )

@router.get("/{task_id}", response_model=Task)
def get_task(task_id: int, db: Session = Depends(get_db)):
    """获取任务信息"""
    db_task = get_task_by_id(db, task_id=task_id)
    if db_task is None:
        raise HTTPException(status_code=404, detail="任务未找到")
    return db_task

@router.get("/user/{user_id}", response_model=list[Task])
def get_user_tasks(user_id: int, db: Session = Depends(get_db)):
    """获取用户的所有任务"""
    return get_tasks_by_user_id(db, user_id=user_id)
