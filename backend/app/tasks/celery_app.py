"""Celery application configuration."""

from celery import Celery

from app.core.config import get_settings

settings = get_settings()

celery_app = Celery(
    "filepassword",
    broker=settings.celery_broker_url,
    backend=settings.celery_result_backend,
    include=[
        "app.tasks.crack_tasks",
        "app.tasks.file_tasks",
        "app.tasks.notification_tasks",
        "app.tasks.cleanup_tasks",
    ],
)

# Configure Celery
celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="Asia/Shanghai",
    enable_utc=True,
    task_track_started=True,
    task_time_limit=30 * 60,  # 30 minutes
    task_soft_time_limit=25 * 60,  # 25 minutes
    worker_prefetch_multiplier=4,
    worker_max_tasks_per_child=1000,
)

# Configure beat schedule
celery_app.conf.beat_schedule = {
    "cleanup-expired-files": {
        "task": "app.tasks.cleanup_tasks.cleanup_expired_files",
        "schedule": 5.0,  # every 5 minutes for testing, should be 1 hour in production
    },
    "cleanup-old-logs": {
        "task": "app.tasks.cleanup_tasks.cleanup_old_logs",
        "schedule": 3600.0,  # every hour
    },
}

if __name__ == "__main__":
    celery_app.start()
