from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.file import File as FileSchema, FileCreate, FileResponse
from app.crud.file import create_file, get_file_by_id, get_files_by_user_id
from app.core.config import settings
import shutil
import os

router = APIRouter()

@router.post("/upload", response_model=FileResponse)
def upload_file(
    file: UploadFile = File(...),
    email: str = Form(...),
    crack_type: str = Form(...),
    db: Session = Depends(get_db)
):
    """上传文件"""
    # 检查文件大小
    if file.size > settings.MAX_FILE_SIZE:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail=f"文件大小超过限制，最大允许{settings.MAX_FILE_SIZE / 1024 / 1024}MB"
        )
    
    # 保存文件
    file_path = os.path.join(settings.FILE_STORAGE_PATH, file.filename)
    os.makedirs(settings.FILE_STORAGE_PATH, exist_ok=True)
    
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    # 创建文件记录
    file_data = FileCreate(
        filename=file.filename,
        file_path=file_path,
        size=file.size,
        content_type=file.content_type
    )
    
    db_file = create_file(db=db, file=file_data)
    
    return FileResponse(
        id=db_file.id,
        filename=db_file.filename,
        size=db_file.size,
        content_type=db_file.content_type,
        created_at=db_file.created_at
    )

@router.get("/{file_id}", response_model=FileSchema)
def get_file(file_id: int, db: Session = Depends(get_db)):
    """获取文件信息"""
    db_file = get_file_by_id(db, file_id=file_id)
    if db_file is None:
        raise HTTPException(status_code=404, detail="文件未找到")
    return db_file
