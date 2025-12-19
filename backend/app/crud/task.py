from sqlalchemy.orm import Session
from app.models.task import Task, TaskStatus
from app.schemas.task import TaskCreate

def get_task_by_id(db: Session, task_id: int):
    """通过ID获取任务"""
    return db.query(Task).filter(Task.id == task_id).first()

def get_tasks_by_user_id(db: Session, user_id: int, skip: int = 0, limit: int = 100):
    """获取用户的所有任务"""
    return db.query(Task).filter(Task.user_id == user_id).offset(skip).limit(limit).all()

def create_task(db: Session, task: TaskCreate):
    """创建新任务"""
    # 根据破解类型设置估计时间
    estimated_time = {
        "simple": 3600,  # 1小时
        "regular": 24 * 3600,  # 1天
        "professional": 7 * 24 * 3600  # 7天
    }.get(task.crack_type, 24 * 3600)
    
    db_task = Task(
        file_id=task.file_id,
        user_id=task.user_id,
        email=task.email,
        crack_type=task.crack_type,
        status=TaskStatus.PENDING,
        estimated_time=estimated_time
    )
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

def update_task_status(db: Session, task_id: int, status: TaskStatus, result: str = None):
    """更新任务状态"""
    db_task = db.query(Task).filter(Task.id == task_id).first()
    if db_task:
        db_task.status = status
        if result:
            db_task.result = result
        db.commit()
        db.refresh(db_task)
        return db_task
    return None
