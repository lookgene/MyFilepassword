from sqlalchemy.orm import Session
from app.models.file import File
from app.schemas.file import FileCreate

def get_file_by_id(db: Session, file_id: int):
    """通过ID获取文件"""
    return db.query(File).filter(File.id == file_id).first()

def get_files_by_user_id(db: Session, user_id: int, skip: int = 0, limit: int = 100):
    """获取用户的所有文件"""
    return db.query(File).filter(File.user_id == user_id).offset(skip).limit(limit).all()

def create_file(db: Session, file: FileCreate):
    """创建新文件记录"""
    db_file = File(
        filename=file.filename,
        file_path=file.file_path,
        size=file.size,
        content_type=file.content_type,
        user_id=file.user_id
    )
    db.add(db_file)
    db.commit()
    db.refresh(db_file)
    return db_file

def delete_file(db: Session, file_id: int):
    """删除文件"""
    db_file = db.query(File).filter(File.id == file_id).first()
    if db_file:
        db.delete(db_file)
        db.commit()
        return True
    return False
