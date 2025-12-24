"""Cleanup tasks."""

from app.tasks.celery_app import celery_app


@celery_app.task(name="app.tasks.cleanup_tasks.cleanup_expired_files")
def cleanup_expired_files():
    """Clean up expired uploaded files."""
    # TODO: Implement file cleanup logic
    pass


@celery_app.task(name="app.tasks.cleanup_tasks.cleanup_old_logs")
def cleanup_old_logs():
    """Clean up old task logs."""
    # TODO: Implement log cleanup logic
    pass
