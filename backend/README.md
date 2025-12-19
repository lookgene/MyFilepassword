# 在线加密文件解密服务 - 后端部署说明

## 1. 项目概述

本项目是在线加密文件解密服务的后端部分，基于FastAPI开发，提供了文件上传、破解任务管理、支付处理等核心功能。

## 2. 技术栈

- 框架：FastAPI
- 语言：Python 3.10+
- 数据库：PostgreSQL
- 缓存：Redis
- 消息队列：RabbitMQ
- 任务队列：Celery
- ORM：SQLAlchemy
- 认证：JWT

## 3. 环境要求

- Python：>= 3.10
- PostgreSQL：>= 13.0
- Redis：>= 6.0
- RabbitMQ：>= 3.8

## 4. 安装依赖

1. 进入后端项目目录
```bash
cd backend
```

2. 创建Python虚拟环境
```bash
# 使用venv创建虚拟环境
python -m venv venv

# 激活虚拟环境
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate
```

3. 安装依赖
```bash
pip install -r requirements.txt
```

## 5. 数据库配置

### 5.1 创建数据库

1. 登录PostgreSQL
```bash
psql -U postgres
```

2. 创建数据库
```sql
CREATE DATABASE file_decryption;
CREATE USER postgres WITH PASSWORD 'password';
GRANT ALL PRIVILEGES ON DATABASE file_decryption TO postgres;
```

### 5.2 数据库迁移

使用Alembic进行数据库迁移：

1. 初始化Alembic（如果尚未初始化）
```bash
alembic init alembic
```

2. 修改`alembic.ini`中的数据库连接字符串
```ini
sqlalchemy.url = postgresql://postgres:password@localhost:5432/file_decryption
```

3. 创建迁移脚本
```bash
alembic revision --autogenerate -m "Initial migration"
```

4. 执行迁移
```bash
alembic upgrade head
```

## 6. 开发环境运行

### 6.1 启动主应用

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

API文档将在以下地址可用：
- Swagger UI：http://localhost:8000/docs
- ReDoc：http://localhost:8000/redoc

### 6.2 启动Celery Worker

```bash
celery -A app.services.crack.celery worker --loglevel=info
```

### 6.3 启动Celery Beat（可选，用于定时任务）

```bash
celery -A app.services.crack.celery beat --loglevel=info
```

## 7. 生产环境部署

### 7.1 使用Gunicorn + Uvicorn

```bash
# 安装Gunicorn
pip install gunicorn

# 启动应用
# 注意：根据服务器配置调整worker数量
# -w 4: 使用4个worker进程
# -k uvicorn.workers.UvicornWorker: 使用Uvicorn作为worker类
# app.main:app: 应用入口
# --bind 0.0.0.0:8000: 绑定到所有网络接口的8000端口
# --log-level info: 日志级别为info
# --access-logfile -: 访问日志输出到标准输出
# --error-logfile -: 错误日志输出到标准输出
# --daemon: 后台运行

# 前台运行
# gunicorn -w 4 -k uvicorn.workers.UvicornWorker app.main:app --bind 0.0.0.0:8000 --log-level info --access-logfile - --error-logfile -

# 后台运行
# gunicorn -w 4 -k uvicorn.workers.UvicornWorker app.main:app --bind 0.0.0.0:8000 --log-level info --access-logfile - --error-logfile - --daemon
```

### 7.2 使用Docker部署

1. 创建Dockerfile
```dockerfile
FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

2. 创建docker-compose.yml
```yaml
version: '3'

services:
  app:
    build: .
    ports:
      - "8000:8000"
    depends_on:
      - db
      - redis
      - rabbitmq
    environment:
      - DATABASE_URL=postgresql://postgres:password@db:5432/file_decryption
      - REDIS_URL=redis://redis:6379/0
      - RABBITMQ_URL=amqp://guest:guest@rabbitmq:5672/
    volumes:
      - ./uploads:/app/uploads

  db:
    image: postgres:13
    environment:
      - POSTGRES_DB=file_decryption
      - POSTGRES_USER=postgres
      - POSTGRES_PASSWORD=password
    volumes:
      - postgres_data:/var/lib/postgresql/data

  redis:
    image: redis:6
    volumes:
      - redis_data:/data

  rabbitmq:
    image: rabbitmq:3.8
    volumes:
      - rabbitmq_data:/var/lib/rabbitmq

  celery-worker:
    build: .
    command: celery -A app.services.crack.celery worker --loglevel=info
    depends_on:
      - app
      - db
      - redis
      - rabbitmq
    environment:
      - DATABASE_URL=postgresql://postgres:password@db:5432/file_decryption
      - REDIS_URL=redis://redis:6379/0
      - RABBITMQ_URL=amqp://guest:guest@rabbitmq:5672/
    volumes:
      - ./uploads:/app/uploads

volumes:
  postgres_data:
  redis_data:
  rabbitmq_data:
```

3. 启动服务
```bash
docker-compose up -d
```

## 8. 配置说明

### 8.1 环境变量

创建 `.env` 文件，配置以下环境变量：

```env
# 应用配置
APP_NAME=在线加密文件解密服务
APP_VERSION=1.0.0
DEBUG=True

# 安全配置
SECRET_KEY=your-secret-key
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7

# 数据库配置
DATABASE_URL=postgresql://postgres:password@localhost:5432/file_decryption

# Redis配置
REDIS_URL=redis://localhost:6379/0

# RabbitMQ配置
RABBITMQ_URL=amqp://guest:guest@localhost:5672/

# CORS配置
CORS_ORIGINS=http://localhost:3000,http://localhost:3001

# 文件存储配置
FILE_STORAGE_PATH=./uploads
MAX_FILE_SIZE=104857600  # 100MB

# 破解引擎配置
HASHCAT_PATH=/usr/bin/hashcat
MAX_CRACK_TIME=604800  # 7天
```

### 8.2 核心配置文件

- `app/core/config.py`：应用核心配置
- `app/core/database.py`：数据库连接配置

## 9. 项目结构

```
backend/
├── app/                   # 主应用目录
│   ├── api/               # API路由
│   ├── core/              # 核心配置
│   ├── crud/              # CRUD操作
│   ├── models/            # 数据库模型
│   ├── schemas/           # Pydantic模型
│   ├── services/          # 业务逻辑
│   └── main.py            # 应用入口
├── config/                # 配置文件
├── scripts/               # 脚本文件
├── tests/                 # 测试文件
├── uploads/               # 文件上传目录
├── requirements.txt       # 依赖列表
└── README.md              # 部署说明
```

## 10. 常见问题

### 10.1 数据库连接失败

**问题**：无法连接到PostgreSQL数据库

**解决方案**：
- 检查PostgreSQL是否正在运行
- 检查数据库连接字符串是否正确
- 确保数据库用户具有正确的权限

### 10.2 Redis连接失败

**问题**：无法连接到Redis

**解决方案**：
- 检查Redis是否正在运行
- 检查Redis连接字符串是否正确
- 确保Redis端口没有被防火墙阻止

### 10.3 RabbitMQ连接失败

**问题**：无法连接到RabbitMQ

**解决方案**：
- 检查RabbitMQ是否正在运行
- 检查RabbitMQ连接字符串是否正确
- 确保RabbitMQ端口没有被防火墙阻止

### 10.4 Celery任务执行失败

**问题**：Celery任务无法正常执行

**解决方案**：
- 检查Celery worker是否正在运行
- 检查任务队列配置是否正确
- 查看Celery日志以获取详细错误信息

## 11. 监控与维护

### 11.1 日志监控

应用日志默认输出到标准输出，可以通过以下方式收集和监控：

- 使用ELK Stack（Elasticsearch + Logstash + Kibana）收集和分析日志
- 使用Prometheus + Grafana监控应用指标

### 11.2 性能优化

- 数据库索引优化：为频繁查询的字段添加索引
- 缓存优化：合理使用Redis缓存热点数据
- 任务队列优化：根据任务类型调整Celery worker数量
- 定期清理过期文件：设置定时任务清理过期的上传文件和任务结果

## 12. 联系方式

如有问题，请联系项目开发团队。
