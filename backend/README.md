# FilePassword Backend

在线加密文件解密SAAS平台后端服务

## 技术栈

- Python 3.10+
- FastAPI 0.104+
- SQLAlchemy 2.0+ (异步ORM)
- PostgreSQL 15+
- Redis 7+
- Celery 5.3+
- RabbitMQ 3.12+
- MinIO / 阿里云OSS (对象存储)
- ClamAV (病毒扫描)

## 项目结构

```
backend/
├── app/
│   ├── api/              # API路由
│   │   └── v1/           # API v1版本
│   │       └── endpoints/ # API端点
│   ├── core/             # 核心配置
│   ├── models/           # 数据库模型
│   ├── schemas/          # Pydantic模式
│   ├── services/         # 业务逻辑
│   ├── tasks/            # Celery任务
│   ├── utils/            # 工具函数
│   ├── middleware/       # 中间件
│   ├── db/               # 数据库
│   ├── storage/          # 存储服务
│   ├── crack/            # 破解引擎
│   └── main.py           # 应用入口
├── tests/                # 测试
├── scripts/              # 脚本
├── alembic/              # 数据库迁移
├── logs/                 # 日志文件
├── crack/                # 破解工作目录
├── pyproject.toml        # 项目配置
├── Dockerfile            # Docker镜像
└── docker-compose.yml    # Docker Compose配置
```

## 快速开始

### 方式一：使用启动脚本（推荐）

**Linux/Mac:**
```bash
cd backend
chmod +x scripts/dev.sh
./scripts/dev.sh
```

**Windows:**
```bash
cd backend
scripts\dev.bat
```

### 方式二：手动启动

#### 1. 启动依赖服务

```bash
# 启动所有依赖服务（PostgreSQL、Redis、RabbitMQ、MinIO）
docker-compose up -d db redis rabbitmq minio

# 查看服务状态
docker-compose ps
```

#### 2. 安装依赖

```bash
# 创建虚拟环境
python -m venv venv

# 激活虚拟环境
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# 安装依赖
pip install -e ".[dev]"
```

#### 3. 配置环境变量

```bash
# 已提供默认的 .env 文件用于本地开发
# 生产环境请修改以下配置:
# - SECRET_KEY
# - JWT_SECRET_KEY
# - 数据库密码
# - 对象存储配置
```

#### 4. 初始化数据库

```bash
# 运行数据库迁移
alembic upgrade head

# 创建管理员用户
python scripts/init_db.py
```

#### 5. 启动应用服务

**终端1 - 启动API服务:**
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**终端2 - 启动Celery Worker:**
```bash
celery -A app.tasks.celery_app worker --loglevel=info --concurrency=4
```

**终端3 - 启动Celery Beat (定时任务):**
```bash
celery -A app.tasks.celery_app beat --loglevel=info
```

**终端4 - 启动Flower (Celery监控):**
```bash
celery -A app.tasks.celery_app flower --port=5555
```

## 访问地址

启动后可访问：

| 服务 | 地址 | 说明 |
|------|------|------|
| API文档 | http://localhost:8000/docs | Swagger UI |
| API文档 | http://localhost:8000/redoc | ReDoc |
| 健康检查 | http://localhost:8000/health | 服务状态 |
| Prometheus | http://localhost:8000/metrics | 指标数据 |
| Flower | http://localhost:5555 | Celery监控 |
| MinIO控制台 | http://localhost:9001 | 对象存储 |
| RabbitMQ管理 | http://localhost:15672 | 消息队列 (admin/admin) |

## 默认账号

创建的管理员账号：
- 邮箱: `admin@example.com`
- 密码: `Admin123!`

## 开发指南

### 代码规范

```bash
# 格式化代码
black app/

# 代码检查
ruff check app/

# 类型检查
mypy app/
```

### 运行测试

```bash
# 运行所有测试
pytest

# 运行测试并生成覆盖率报告
pytest --cov=app --cov-report=html

# 运行特定测试
pytest tests/api/test_auth.py -v
```

### 数据库迁移

```bash
# 创建新的迁移
alembic revision --autogenerate -m "描述"

# 查看迁移历史
alembic history

# 应用迁移
alembic upgrade head

# 回滚迁移
alembic downgrade -1
```

### 日志

日志文件位于 `logs/` 目录：
- `app.log` - 应用日志
- `error.log` - 错误日志

## 已实现的功能

### 核心框架
- [x] FastAPI应用结构
- [x] 异步数据库支持（SQLAlchemy 2.0）
- [x] JWT认证
- [x] CORS中间件
- [x] 请求日志
- [x] 错误处理
- [x] 健康检查

### 数据模型
- [x] 用户模型（User、UserProfile、Membership）
- [x] 文件模型（File）
- [x] 任务模型（Task、TaskLog）
- [x] 支付模型（Order、Refund）
- [x] 通知模型（Notification）
- [x] API密钥模型（ApiKey）
- [x] 优惠券模型（Coupon、UserCoupon）

### API接口
- [x] 认证接口（注册、登录、登出、刷新Token、忘记密码）
- [x] 用户接口（获取信息、更新信息、统计）
- [x] 文件接口（上传URL、确认上传、列表、删除）
- [x] 任务接口（创建、查询、更新、取消）
- [x] 支付接口（创建订单、取消订单、退款）
- [x] 通知接口（列表、标记已读、删除）

### 后台任务
- [x] Celery配置
- [x] 任务调度器（Beat）
- [ ] 文件清理任务
- [ ] 日志清理任务
- [ ] 破解任务

### 待实现功能
- [ ] 文件上传服务（MinIO/OSS）
- [ ] 病毒扫描（ClamAV）
- [ ] 支付集成（微信支付、支付宝）
- [ ] 邮件发送
- [ ] 短信发送
- [ ] 密码破解引擎（Hashcat）
- [ ] WebSocket实时通知

## 部署

### Docker部署

```bash
# 构建镜像
docker build -t filepassword-backend .

# 运行容器
docker run -d -p 8000:8000 --env-file .env filepassword-backend
```

### Docker Compose部署

```bash
# 启动所有服务
docker-compose up -d

# 查看日志
docker-compose logs -f backend

# 停止服务
docker-compose down

# 停止并删除数据
docker-compose down -v
```

### 生产环境配置

生产环境需要修改：
1. `DEBUG=false`
2. 使用强密码作为 `SECRET_KEY` 和 `JWT_SECRET_KEY`
3. 配置生产数据库
4. 配置对象存储（建议使用阿里云OSS或AWS S3）
5. 配置邮件服务
6. 配置支付接口
7. 配置HTTPS

## 许可证

MIT License
