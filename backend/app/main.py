from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import users, files, tasks, payments
from app.core.config import settings

app = FastAPI(
    title="在线加密文件解密API",
    description="专业的在线加密文件解密服务API，支持多种文件格式，提供快速、安全的密码破解方案",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册路由
app.include_router(users.router, prefix="/api/users", tags=["users"])
app.include_router(files.router, prefix="/api/files", tags=["files"])
app.include_router(tasks.router, prefix="/api/tasks", tags=["tasks"])
app.include_router(payments.router, prefix="/api/payments", tags=["payments"])

@app.get("/api/health")
async def health_check():
    return {"status": "ok", "message": "在线加密文件解密API服务正常运行"}