from celery import Celery
from app.core.config import settings
from app.core.database import SessionLocal
from app.crud.task import get_task_by_id, update_task_status
from app.models.task import TaskStatus
from app.services.email import email_service
import subprocess
import os

# 创建Celery实例
celery = Celery(
    "crack_tasks",
    broker=settings.RABBITMQ_URL,
    backend=settings.REDIS_URL
)

@celery.task(name="start_crack_task")
def start_crack_task(task_id: int):
    """启动破解任务"""
    db = SessionLocal()
    try:
        # 获取任务信息
        task = get_task_by_id(db, task_id)
        if not task:
            return
        
        # 更新任务状态为运行中
        update_task_status(db, task_id, TaskStatus.RUNNING)
        
        # 根据破解类型执行不同的破解策略
        if task.crack_type == "simple":
            result = run_simple_crack(task.file_id)
        elif task.crack_type == "regular":
            result = run_regular_crack(task.file_id)
        else:  # professional
            result = run_professional_crack(task.file_id)
        
        # 更新任务结果
        if result:
            update_task_status(db, task_id, TaskStatus.SUCCESS, result)
            # 发送任务成功邮件
            email_service.send_task_completed_email(
                email=task.email,
                task_id=task.id,
                result=result,
                success=True
            )
        else:
            update_task_status(db, task_id, TaskStatus.FAILED, "破解失败")
            # 发送任务失败邮件
            email_service.send_task_completed_email(
                email=task.email,
                task_id=task.id,
                result="破解失败，无法找到正确密码",
                success=False
            )
    finally:
        db.close()

def run_simple_crack(file_id: int):
    """执行简单密码破解（6位纯数字）"""
    # 这里只是示例，实际需要调用Hashcat或自定义算法
    try:
        # 模拟破解过程
        import time
        time.sleep(30)  # 模拟30秒的破解时间
        return "123456"  # 模拟破解结果
    except Exception as e:
        print(f"简单破解失败: {e}")
        return None

def run_regular_crack(file_id: int):
    """执行常规密码破解（字母、数字、符号组合）"""
    try:
        # 模拟破解过程
        import time
        time.sleep(60)  # 模拟1分钟的破解时间
        return "Password123!"  # 模拟破解结果
    except Exception as e:
        print(f"常规破解失败: {e}")
        return None

def run_professional_crack(file_id: int):
    """执行专业密码破解（高级算法）"""
    try:
        # 模拟破解过程
        import time
        time.sleep(120)  # 模拟2分钟的破解时间
        return "ComplexPassword@2025"  # 模拟破解结果
    except Exception as e:
        print(f"专业破解失败: {e}")
        return None

def call_hashcat(file_path: str, crack_type: str):
    """调用Hashcat进行密码破解"""
    # 构建Hashcat命令
    hashcat_path = settings.HASHCAT_PATH
    
    # 根据破解类型选择不同的模式
    if crack_type == "simple":
        # 6位纯数字字典攻击
        command = [
            hashcat_path,
            "-a", "3",  # 暴力破解模式
            "-m", "1400",  # SHA-256模式（示例）
            file_path,
            "?d?d?d?d?d?d"  # 6位数字掩码
        ]
    elif crack_type == "regular":
        # 字母数字符号组合
        command = [
            hashcat_path,
            "-a", "3",
            "-m", "1400",
            file_path,
            "?a?a?a?a?a?a?a?a"  # 8位任意字符
        ]
    else:  # professional
        # 高级模式，使用字典+规则
        command = [
            hashcat_path,
            "-a", "0",  # 字典攻击模式
            "-m", "1400",
            file_path,
            "/path/to/rockyou.txt",  # 示例字典路径
            "-r", "/path/to/rules/best64.rule"  # 示例规则文件
        ]
    
    try:
        # 执行Hashcat命令
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            timeout=settings.MAX_CRACK_TIME
        )
        
        # 解析Hashcat输出，提取密码
        # 注意：实际解析逻辑需要根据Hashcat的输出格式进行调整
        if result.returncode == 0:
            # 模拟解析结果
            return "cracked_password"
        return None
    except subprocess.TimeoutExpired:
        print(f"破解超时")
        return None
    except Exception as e:
        print(f"Hashcat调用失败: {e}")
        return None
