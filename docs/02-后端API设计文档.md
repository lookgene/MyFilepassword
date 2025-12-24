# 在线加密文件解密SAAS平台 - 后端API设计文档

## 1. 文档说明

### 1.1 文档目的
本文档详细描述后端API接口设计，包括请求参数、响应格式、错误码等内容，供前后端开发人员参考。

### 1.2 基础信息
- **Base URL（开发）**: `http://localhost:8000/api/v1`
- **Base URL（生产）**: `https://api.example.com/api/v1`
- **协议**: HTTPS
- **数据格式**: JSON
- **字符编码**: UTF-8

### 1.3 通用说明

#### 1.3.1 请求头
```http
Content-Type: application/json
Authorization: Bearer {jwt_token}
Accept-Language: zh-CN
X-Request-ID: {uuid}
```

#### 1.3.2 响应格式
成功响应：
```json
{
  "code": 0,
  "message": "success",
  "data": {},
  "timestamp": "2024-01-01T00:00:00Z"
}
```

错误响应：
```json
{
  "code": 1001,
  "message": "参数验证失败",
  "errors": {
    "email": "邮箱格式不正确"
  },
  "timestamp": "2024-01-01T00:00:00Z"
}
```

#### 1.3.3 分页参数
```json
{
  "page": 1,
  "page_size": 20
}
```

#### 1.3.4 分页响应
```json
{
  "code": 0,
  "message": "success",
  "data": {
    "items": [],
    "total": 100,
    "page": 1,
    "page_size": 20,
    "pages": 5
  }
}
```

## 2. 错误码定义

| 错误码 | 说明 | HTTP状态码 |
|--------|------|-----------|
| 0 | 成功 | 200 |
| 1001 | 参数验证失败 | 400 |
| 1002 | 缺少必填参数 | 400 |
| 1003 | 参数格式错误 | 400 |
| 2001 | 未认证 | 401 |
| 2002 | Token过期 | 401 |
| 2003 | Token无效 | 401 |
| 3001 | 无权限 | 403 |
| 3002 | 资源不可访问 | 403 |
| 4001 | 资源不存在 | 404 |
| 4002 | 用户不存在 | 404 |
| 4003 | 任务不存在 | 404 |
| 5001 | 资源已存在 | 409 |
| 5002 | 邮箱已被注册 | 409 |
| 5003 | 任务名称重复 | 409 |
| 6001 | 超过速率限制 | 429 |
| 7001 | 文件过大 | 400 |
| 7002 | 文件格式不支持 | 400 |
| 7003 | 文件上传失败 | 500 |
| 8001 | 支付失败 | 500 |
| 8002 | 退款失败 | 500 |
| 9001 | 破解失败 | 500 |
| 9002 | 破解引擎异常 | 500 |
| 9999 | 服务器内部错误 | 500 |

## 3. 认证授权API

### 3.1 用户注册

**接口**: `POST /auth/register`

**请求参数**:
```json
{
  "email": "user@example.com",
  "password": "Password123!",
  "confirm_password": "Password123!",
  "invite_code": "ABC123"  // 可选
}
```

**响应**:
```json
{
  "code": 0,
  "message": "注册成功",
  "data": {
    "user_id": "uuid",
    "email": "user@example.com",
    "access_token": "jwt_token",
    "refresh_token": "refresh_token",
    "expires_in": 7200
  }
}
```

### 3.2 用户登录

**接口**: `POST /auth/login`

**请求参数**:
```json
{
  "email": "user@example.com",
  "password": "Password123!"
}
```

**响应**:
```json
{
  "code": 0,
  "message": "登录成功",
  "data": {
    "user_id": "uuid",
    "email": "user@example.com",
    "username": "用户名",
    "avatar": "https://...",
    "membership": "premium",
    "access_token": "jwt_token",
    "refresh_token": "refresh_token",
    "expires_in": 7200
  }
}
```

### 3.3 刷新Token

**接口**: `POST /auth/refresh`

**请求参数**:
```json
{
  "refresh_token": "refresh_token"
}
```

**响应**:
```json
{
  "code": 0,
  "data": {
    "access_token": "new_jwt_token",
    "expires_in": 7200
  }
}
```

### 3.4 用户登出

**接口**: `POST /auth/logout`

**请求头**: `Authorization: Bearer {jwt_token}`

**响应**:
```json
{
  "code": 0,
  "message": "登出成功"
}
```

### 3.5 忘记密码

**接口**: `POST /auth/forgot-password`

**请求参数**:
```json
{
  "email": "user@example.com"
}
```

**响应**:
```json
{
  "code": 0,
  "message": "重置邮件已发送"
}
```

### 3.6 重置密码

**接口**: `POST /auth/reset-password`

**请求参数**:
```json
{
  "token": "reset_token",
  "password": "NewPassword123!",
  "confirm_password": "NewPassword123!"
}
```

**响应**:
```json
{
  "code": 0,
  "message": "密码重置成功"
}
```

### 3.7 修改密码

**接口**: `POST /auth/change-password`

**请求头**: `Authorization: Bearer {jwt_token}`

**请求参数**:
```json
{
  "old_password": "OldPassword123!",
  "new_password": "NewPassword123!"
}
```

**响应**:
```json
{
  "code": 0,
  "message": "密码修改成功"
}
```

## 4. 用户管理API

### 4.1 获取当前用户信息

**接口**: `GET /users/me`

**请求头**: `Authorization: Bearer {jwt_token}`

**响应**:
```json
{
  "code": 0,
  "data": {
    "user_id": "uuid",
    "email": "user@example.com",
    "username": "用户名",
    "avatar": "https://...",
    "phone": "13800138000",
    "membership": "premium",
    "membership_expire": "2024-12-31T23:59:59Z",
    "created_at": "2024-01-01T00:00:00Z",
    "stats": {
      "total_tasks": 100,
      "success_tasks": 85,
      "pending_tasks": 5,
      "total_spent": 999.00
    }
  }
}
```

### 4.2 更新用户信息

**接口**: `PATCH /users/me`

**请求头**: `Authorization: Bearer {jwt_token}`

**请求参数**:
```json
{
  "username": "新用户名",
  "phone": "13900139000",
  "avatar": "base64_image_data"
}
```

**响应**:
```json
{
  "code": 0,
  "message": "更新成功",
  "data": {
    "user_id": "uuid",
    "email": "user@example.com",
    "username": "新用户名",
    "avatar": "https://..."
  }
}
```

### 4.3 获取用户会员信息

**接口**: `GET /users/me/membership`

**请求头**: `Authorization: Bearer {jwt_token}`

**响应**:
```json
{
  "code": 0,
  "data": {
    "membership": "premium",
    "expire_at": "2024-12-31T23:59:59Z",
    "benefits": {
      "discount": 0.9,
      "max_concurrent_tasks": 3,
      "priority": "high"
    },
    "can_upgrade": true
  }
}
```

### 4.4 购买会员

**接口**: `POST /users/me/membership/subscribe`

**请求头**: `Authorization: Bearer {jwt_token}`

**请求参数**:
```json
{
  "plan": "premium",
  "duration": 1,
  "payment_method": "wechat"
}
```

**响应**:
```json
{
  "code": 0,
  "data": {
    "order_id": "uuid",
    "payment_url": "https://...",
    "qr_code": "base64_qr_code"
  }
}
```

### 4.5 续费会员

**接口**: `POST /users/me/membership/renew`

**请求头**: `Authorization: Bearer {jwt_token}`

**请求参数**:
```json
{
  "duration": 1
}
```

**响应**:
```json
{
  "code": 0,
  "data": {
    "order_id": "uuid",
    "amount": 99.00,
    "payment_url": "https://..."
  }
}
```

### 4.6 取消会员

**接口**: `POST /users/me/membership/cancel`

**请求头**: `Authorization: Bearer {jwt_token}`

**响应**:
```json
{
  "code": 0,
  "message": "会员已取消，到期后将不再续费"
}
```

### 4.7 获取用户任务列表

**接口**: `GET /users/me/tasks`

**请求头**: `Authorization: Bearer {jwt_token}`

**查询参数**:
```
page=1&page_size=20&status=processing&order_by=created_at&order=desc
```

**响应**:
```json
{
  "code": 0,
  "data": {
    "items": [
      {
        "task_id": "uuid",
        "task_name": "任务名称",
        "file_name": "document.zip",
        "file_size": 1024000,
        "crack_type": "simple",
        "status": "processing",
        "progress": 50,
        "created_at": "2024-01-01T00:00:00Z",
        "estimated_time": "2024-01-01T00:10:00Z"
      }
    ],
    "total": 100,
    "page": 1,
    "page_size": 20,
    "pages": 5
  }
}
```

### 4.8 获取用户统计信息

**接口**: `GET /users/me/stats`

**请求头**: `Authorization: Bearer {jwt_token}`

**查询参数**: `period=week` (day/week/month/year)

**响应**:
```json
{
  "code": 0,
  "data": {
    "total_tasks": 100,
    "success_tasks": 85,
    "failed_tasks": 10,
    "pending_tasks": 5,
    "total_spent": 999.00,
    "success_rate": 0.85,
    "average_time": 300,
    "daily_stats": [
      {
        "date": "2024-01-01",
        "tasks": 10,
        "success": 8,
        "spent": 99.00
      }
    ]
  }
}
```

## 5. 文件管理API

### 5.1 获取文件上传预签名URL

**接口**: `POST /files/upload-url`

**请求头**: `Authorization: Bearer {jwt_token}`

**请求参数**:
```json
{
  "file_name": "document.zip",
  "file_size": 1024000,
  "content_type": "application/zip"
}
```

**响应**:
```json
{
  "code": 0,
  "data": {
    "upload_url": "https://storage.example.com/...",
    "file_id": "uuid",
    "expires_in": 3600,
    "max_file_size": 52428800
  }
}
```

### 5.2 确认文件上传完成

**接口**: `POST /files/{file_id}/confirm`

**请求头**: `Authorization: Bearer {jwt_token}`

**请求参数**:
```json
{
  "etag": "file_etag",
  "file_size": 1024000
}
```

**响应**:
```json
{
  "code": 0,
  "data": {
    "file_id": "uuid",
    "file_name": "document.zip",
    "file_size": 1024000,
    "file_type": "zip",
    "status": "uploaded",
    "created_at": "2024-01-01T00:00:00Z"
  }
}
```

### 5.3 获取文件列表

**接口**: `GET /files`

**请求头**: `Authorization: Bearer {jwt_token}`

**查询参数**:
```
page=1&page_size=20&file_type=zip&order_by=created_at&order=desc
```

**响应**:
```json
{
  "code": 0,
  "data": {
    "items": [
      {
        "file_id": "uuid",
        "file_name": "document.zip",
        "file_size": 1024000,
        "file_type": "zip",
        "status": "uploaded",
        "task_id": "task_uuid",
        "created_at": "2024-01-01T00:00:00Z"
      }
    ],
    "total": 50,
    "page": 1,
    "page_size": 20
  }
}
```

### 5.4 获取文件详情

**接口**: `GET /files/{file_id}`

**请求头**: `Authorization: Bearer {jwt_token}`

**响应**:
```json
{
  "code": 0,
  "data": {
    "file_id": "uuid",
    "file_name": "document.zip",
    "file_size": 1024000,
    "file_type": "zip",
    "md5": "file_md5_hash",
    "sha256": "file_sha256_hash",
    "status": "uploaded",
    "is_encrypted": true,
    "encryption_info": {
      "algorithm": "AES-256",
      "has_password": true
    },
    "task_id": "task_uuid",
    "created_at": "2024-01-01T00:00:00Z",
    "expires_at": "2024-01-08T00:00:00Z"
  }
}
```

### 5.5 删除文件

**接口**: `DELETE /files/{file_id}`

**请求头**: `Authorization: Bearer {jwt_token}`

**响应**:
```json
{
  "code": 0,
  "message": "文件已删除"
}
```

### 5.6 批量删除文件

**接口**: `DELETE /files/batch`

**请求头**: `Authorization: Bearer {jwt_token}`

**请求参数**:
```json
{
  "file_ids": ["uuid1", "uuid2", "uuid3"]
}
```

**响应**:
```json
{
  "code": 0,
  "message": "已删除3个文件",
  "data": {
    "deleted_count": 3,
    "failed_count": 0
  }
}
```

### 5.7 下载文件

**接口**: `GET /files/{file_id}/download`

**请求头**: `Authorization: Bearer {jwt_token}`

**响应**: 重定向到文件下载URL

### 5.8 病毒扫描状态

**接口**: `GET /files/{file_id}/scan-status`

**请求头**: `Authorization: Bearer {jwt_token}`

**响应**:
```json
{
  "code": 0,
  "data": {
    "file_id": "uuid",
    "scan_status": "clean",
    "scan_result": "No threats found",
    "scanned_at": "2024-01-01T00:00:00Z"
  }
}
```

## 6. 任务管理API

### 6.1 创建破解任务

**接口**: `POST /tasks`

**请求头**: `Authorization: Bearer {jwt_token}`

**请求参数**:
```json
{
  "task_name": "任务名称",
  "file_id": "uuid",
  "crack_type": "simple",
  "crack_config": {
    "password_length": 6,
    "password_type": "numeric",
    "charset": "0123456789",
    "password_hint": "生日是1990年"
  },
  "notification": {
    "email": true,
    "sms": false,
    "webhook": "https://example.com/webhook"
  }
}
```

**crack_type枚举**:
- `simple`: 简单密码（6位纯数字）
- `normal`: 常规任务（复杂密码）
- `advanced`: 专业破解（GPU加速）

**响应**:
```json
{
  "code": 0,
  "data": {
    "task_id": "uuid",
    "task_name": "任务名称",
    "status": "pending",
    "estimated_time": 300,
    "estimated_cost": 0.00,
    "created_at": "2024-01-01T00:00:00Z"
  }
}
```

### 6.2 获取任务列表

**接口**: `GET /tasks`

**请求头**: `Authorization: Bearer {jwt_token}`

**查询参数**:
```
page=1&page_size=20&status=processing&crack_type=simple&order_by=created_at&order=desc
```

**响应**:
```json
{
  "code": 0,
  "data": {
    "items": [
      {
        "task_id": "uuid",
        "task_name": "任务名称",
        "file_name": "document.zip",
        "file_size": 1024000,
        "crack_type": "simple",
        "crack_config": {
          "password_length": 6,
          "password_type": "numeric"
        },
        "status": "processing",
        "progress": 50,
        "current_password": "123456",
        "created_at": "2024-01-01T00:00:00Z",
        "started_at": "2024-01-01T00:01:00Z",
        "estimated_completion": "2024-01-01T00:05:00Z"
      }
    ],
    "total": 100,
    "page": 1,
    "page_size": 20
  }
}
```

**status枚举**:
- `pending`: 等待中
- `queued`: 队列中
- `analyzing`: 分析中
- `processing`: 处理中
- `completed`: 已完成
- `failed`: 失败
- `cancelled`: 已取消

### 6.3 获取任务详情

**接口**: `GET /tasks/{task_id}`

**请求头**: `Authorization: Bearer {jwt_token}`

**响应**:
```json
{
  "code": 0,
  "data": {
    "task_id": "uuid",
    "task_name": "任务名称",
    "file": {
      "file_id": "uuid",
      "file_name": "document.zip",
      "file_size": 1024000,
      "file_type": "zip"
    },
    "crack_type": "simple",
    "crack_config": {
      "password_length": 6,
      "password_type": "numeric",
      "charset": "0123456789",
      "password_hint": "生日是1990年"
    },
    "status": "completed",
    "progress": 100,
    "result": {
      "password": "123456",
      "attempts": 123456,
      "duration": 120
    },
    "cost": 0.00,
    "created_at": "2024-01-01T00:00:00Z",
    "started_at": "2024-01-01T00:01:00Z",
    "completed_at": "2024-01-01T00:03:00Z"
  }
}
```

### 6.4 更新任务

**接口**: `PATCH /tasks/{task_id}`

**请求头**: `Authorization: Bearer {jwt_token}`

**请求参数**:
```json
{
  "task_name": "新任务名称",
  "crack_config": {
    "password_hint": "新提示信息"
  }
}
```

**响应**:
```json
{
  "code": 0,
  "message": "任务已更新",
  "data": {
    "task_id": "uuid",
    "task_name": "新任务名称"
  }
}
```

### 6.5 取消任务

**接口**: `POST /tasks/{task_id}/cancel`

**请求头**: `Authorization: Bearer {jwt_token}`

**响应**:
```json
{
  "code": 0,
  "message": "任务已取消",
  "data": {
    "task_id": "uuid",
    "status": "cancelled",
    "refund_amount": 14.50
  }
}
```

### 6.6 重试任务

**接口**: `POST /tasks/{task_id}/retry`

**请求头**: `Authorization: Bearer {jwt_token}`

**请求参数**:
```json
{
  "crack_config": {
    "password_hint": "新的提示信息"
  }
}
```

**响应**:
```json
{
  "code": 0,
  "message": "任务已重新提交",
  "data": {
    "task_id": "uuid",
    "status": "pending"
  }
}
```

### 6.7 删除任务

**接口**: `DELETE /tasks/{task_id}`

**请求头**: `Authorization: Bearer {jwt_token}`

**响应**:
```json
{
  "code": 0,
  "message": "任务已删除"
}
```

### 6.8 获取任务日志

**接口**: `GET /tasks/{task_id}/logs`

**请求头**: `Authorization: Bearer {jwt_token}`

**查询参数**: `page=1&page_size=50&level=info`

**响应**:
```json
{
  "code": 0,
  "data": {
    "items": [
      {
        "log_id": "uuid",
        "level": "info",
        "message": "任务开始处理",
        "timestamp": "2024-01-01T00:01:00Z"
      },
      {
        "log_id": "uuid",
        "level": "info",
        "message": "尝试密码: 123456",
        "timestamp": "2024-01-01T00:02:00Z"
      }
    ],
    "total": 100
  }
}
```

### 6.9 获取任务进度（SSE）

**接口**: `GET /tasks/{task_id}/progress-stream`

**请求头**: `Authorization: Bearer {jwt_token}`
`Accept: text/event-stream`

**响应**（SSE流）:
```
data: {"task_id":"uuid","progress":10,"status":"processing","current_password":"123456"}

data: {"task_id":"uuid","progress":20,"status":"processing","current_password":"234567"}

data: {"task_id":"uuid","progress":100,"status":"completed","result":{"password":"456789"}}
```

### 6.10 查询匿名任务

**接口**: `GET /tasks/public/{task_id}`

**查询参数**: `email=user@example.com&verify_code=123456`

**响应**:
```json
{
  "code": 0,
  "data": {
    "task_id": "uuid",
    "task_name": "任务名称",
    "file_name": "document.zip",
    "status": "processing",
    "progress": 50,
    "created_at": "2024-01-01T00:00:00Z"
  }
}
```

## 7. 支付管理API

### 7.1 创建订单

**接口**: `POST /payments/orders`

**请求头**: `Authorization: Bearer {jwt_token}`

**请求参数**:
```json
{
  "task_id": "uuid",
  "crack_type": "normal",
  "payment_method": "wechat",
  "coupon_code": "SAVE20"
}
```

**响应**:
```json
{
  "code": 0,
  "data": {
    "order_id": "uuid",
    "order_no": "20240101000001",
    "amount": 29.00,
    "discount": 0.00,
    "final_amount": 29.00,
    "currency": "CNY",
    "status": "pending",
    "expires_at": "2024-01-01T00:30:00Z",
    "payment": {
      "method": "wechat",
      "qr_code": "base64_qr_code",
      "payment_url": "https://..."
    }
  }
}
```

### 7.2 获取订单详情

**接口**: `GET /payments/orders/{order_id}`

**请求头**: `Authorization: Bearer {jwt_token}`

**响应**:
```json
{
  "code": 0,
  "data": {
    "order_id": "uuid",
    "order_no": "20240101000001",
    "task": {
      "task_id": "uuid",
      "task_name": "任务名称"
    },
    "amount": 29.00,
    "discount": 5.80,
    "final_amount": 23.20,
    "currency": "CNY",
    "status": "paid",
    "payment_method": "wechat",
    "paid_at": "2024-01-01T00:05:00Z",
    "created_at": "2024-01-01T00:00:00Z"
  }
}
```

### 7.3 获取订单列表

**接口**: `GET /payments/orders`

**请求头**: `Authorization: Bearer {jwt_token}`

**查询参数**: `page=1&page_size=20&status=paid`

**响应**:
```json
{
  "code": 0,
  "data": {
    "items": [
      {
        "order_id": "uuid",
        "order_no": "20240101000001",
        "amount": 29.00,
        "final_amount": 23.20,
        "status": "paid",
        "created_at": "2024-01-01T00:00:00Z"
      }
    ],
    "total": 50
  }
}
```

### 7.4 取消订单

**接口**: `POST /payments/orders/{order_id}/cancel`

**请求头**: `Authorization: Bearer {jwt_token}`

**响应**:
```json
{
  "code": 0,
  "message": "订单已取消"
}
```

### 7.5 申请退款

**接口**: `POST /payments/orders/{order_id}/refund`

**请求头**: `Authorization: Bearer {jwt_token}`

**请求参数**:
```json
{
  "reason": "任务未完成",
  "amount": 29.00
}
```

**响应**:
```json
{
  "code": 0,
  "data": {
    "refund_id": "uuid",
    "amount": 29.00,
    "status": "processing",
    "estimated_arrival": "1-3个工作日"
  }
}
```

### 7.6 获取退款状态

**接口**: `GET /payments/refunds/{refund_id}`

**请求头**: `Authorization: Bearer {jwt_token}`

**响应**:
```json
{
  "code": 0,
  "data": {
    "refund_id": "uuid",
    "order_id": "uuid",
    "amount": 29.00,
    "status": "completed",
    "reason": "任务未完成",
    "created_at": "2024-01-01T00:00:00Z",
    "completed_at": "2024-01-03T00:00:00Z"
  }
}
```

### 7.7 支付回调（Webhook）

**接口**: `POST /payments/webhook/{provider}`

**provider**: `wechat` | `alipay` | `stripe`

**请求参数**（微信支付）:
```json
{
  "id": "event_id",
  "create_time": "2024-01-01T00:00:00Z",
  "resource_type": "encrypt-resource",
  "event_type": "TRANSACTION.SUCCESS",
  "resource": {
    "algorithm": "AEAD_AES_256_GCM",
    "ciphertext": "encrypted_data",
    "nonce": "nonce",
    "associated_data": "transaction"
  }
}
```

**响应**:
```json
{
  "code": 0,
  "message": "OK"
}
```

### 7.8 验证优惠券

**接口**: `POST /payments/coupons/validate`

**请求头**: `Authorization: Bearer {jwt_token}`

**请求参数**:
```json
{
  "coupon_code": "SAVE20"
}
```

**响应**:
```json
{
  "code": 0,
  "data": {
    "coupon_code": "SAVE20",
    "discount_type": "percent",
    "discount_value": 0.2,
    "min_amount": 10.00,
    "max_discount": 50.00,
    "expires_at": "2024-12-31T23:59:59Z",
    "usable": true
  }
}
```

### 7.9 获取用户优惠券列表

**接口**: `GET /payments/coupons`

**请求头**: `Authorization: Bearer {jwt_token}`

**响应**:
```json
{
  "code": 0,
  "data": {
    "items": [
      {
        "coupon_id": "uuid",
        "coupon_code": "SAVE20",
        "discount": "8折",
        "status": "available",
        "expires_at": "2024-12-31T23:59:59Z"
      }
    ]
  }
}
```

### 7.10 申请发票

**接口**: `POST /payments/invoices`

**请求头**: `Authorization: Bearer {jwt_token}`

**请求参数**:
```json
{
  "order_id": "uuid",
  "invoice_type": "electronic",
  "title": "公司名称",
  "tax_number": "税务登记号",
  "email": "billing@example.com"
}
```

**响应**:
```json
{
  "code": 0,
  "data": {
    "invoice_id": "uuid",
    "invoice_no": "INV2024010100001",
    "status": "processing"
  }
}
```

## 8. 通知管理API

### 8.1 获取通知列表

**接口**: `GET /notifications`

**请求头**: `Authorization: Bearer {jwt_token}`

**查询参数**:
```
page=1&page_size=20&type=task&is_read=false
```

**响应**:
```json
{
  "code": 0,
  "data": {
    "items": [
      {
        "notification_id": "uuid",
        "type": "task_completed",
        "title": "任务完成",
        "content": "您的任务「文档解密」已完成",
        "data": {
          "task_id": "uuid",
          "task_name": "文档解密"
        },
        "is_read": false,
        "created_at": "2024-01-01T00:00:00Z"
      }
    ],
    "total": 50,
    "unread_count": 10
  }
}
```

### 8.2 标记通知已读

**接口**: `POST /notifications/{notification_id}/read`

**请求头**: `Authorization: Bearer {jwt_token}`

**响应**:
```json
{
  "code": 0,
  "message": "已标记为已读"
}
```

### 8.3 批量标记已读

**接口**: `POST /notifications/read-all`

**请求头**: `Authorization: Bearer {jwt_token}`

**请求参数**:
```json
{
  "notification_ids": ["uuid1", "uuid2"]
}
```

**响应**:
```json
{
  "code": 0,
  "message": "已标记2条通知为已读"
}
```

### 8.4 删除通知

**接口**: `DELETE /notifications/{notification_id}`

**请求头**: `Authorization: Bearer {jwt_token}`

**响应**:
```json
{
  "code": 0,
  "message": "通知已删除"
}
```

### 8.5 获取通知设置

**接口**: `GET /notifications/settings`

**请求头**: `Authorization: Bearer {jwt_token}`

**响应**:
```json
{
  "code": 0,
  "data": {
    "email": {
      "task_created": true,
      "task_started": true,
      "task_completed": true,
      "task_failed": true,
      "payment_success": true
    },
    "sms": {
      "task_completed": false,
      "payment_success": false
    },
    "webhook": {
      "enabled": false,
      "url": ""
    }
  }
}
```

### 8.6 更新通知设置

**接口**: `PATCH /notifications/settings`

**请求头**: `Authorization: Bearer {jwt_token}`

**请求参数**:
```json
{
  "email": {
    "task_created": true
  },
  "webhook": {
    "enabled": true,
    "url": "https://example.com/webhook"
  }
}
```

**响应**:
```json
{
  "code": 0,
  "message": "设置已更新"
}
```

## 9. 企业API管理

### 9.1 创建API密钥

**接口**: `POST /api-keys`

**请求头**: `Authorization: Bearer {jwt_token}`

**请求参数**:
```json
{
  "name": "生产环境",
  "scopes": ["tasks:read", "tasks:create", "files:upload"],
  "ip_whitelist": ["192.168.1.1", "192.168.1.2"],
  "rate_limit": 1000
}
```

**响应**:
```json
{
  "code": 0,
  "data": {
    "api_key_id": "uuid",
    "api_key": "sk_live_xxxxxxxxxxxx",
    "name": "生产环境",
    "scopes": ["tasks:read", "tasks:create", "files:upload"],
    "created_at": "2024-01-01T00:00:00Z"
  }
}
```

### 9.2 获取API密钥列表

**接口**: `GET /api-keys`

**请求头**: `Authorization: Bearer {jwt_token}`

**响应**:
```json
{
  "code": 0,
  "data": {
    "items": [
      {
        "api_key_id": "uuid",
        "name": "生产环境",
        "api_key": "sk_live_xxxxxxxxxxxx",
        "scopes": ["tasks:read", "tasks:create"],
        "last_used": "2024-01-01T00:00:00Z",
        "created_at": "2024-01-01T00:00:00Z"
      }
    ]
  }
}
```

### 9.3 删除API密钥

**接口**: `DELETE /api-keys/{api_key_id}`

**请求头**: `Authorization: Bearer {jwt_token}`

**响应**:
```json
{
  "code": 0,
  "message": "API密钥已删除"
}
```

### 9.4 获取API使用统计

**接口**: `GET /api-keys/usage`

**请求头**: `Authorization: Bearer {jwt_token}`

**查询参数**: `period=month`

**响应**:
```json
{
  "code": 0,
  "data": {
    "total_requests": 10000,
    "successful_requests": 9800,
    "failed_requests": 200,
    "rate_limit_exceeded": 50,
    "daily_usage": [
      {
        "date": "2024-01-01",
        "requests": 500
      }
    ]
  }
}
```

### 9.5 企业批量创建任务

**接口**: `POST /enterprise/tasks/batch`

**请求头**: `Authorization: Bearer {jwt_token}` 或 `X-API-Key: {api_key}`

**请求参数**:
```json
{
  "tasks": [
    {
      "task_name": "任务1",
      "file_url": "https://storage.example.com/file1.zip",
      "crack_type": "simple",
      "callback_url": "https://example.com/callback"
    },
    {
      "task_name": "任务2",
      "file_url": "https://storage.example.com/file2.zip",
      "crack_type": "normal",
      "callback_url": "https://example.com/callback"
    }
  ]
}
```

**响应**:
```json
{
  "code": 0,
  "data": {
    "batch_id": "uuid",
    "total": 2,
    "tasks": [
      {
        "task_id": "uuid",
        "status": "pending"
      },
      {
        "task_id": "uuid",
        "status": "pending"
      }
    ]
  }
}
```

## 10. 系统配置API

### 10.1 获取系统配置

**接口**: `GET /config`

**响应**:
```json
{
  "code": 0,
  "data": {
    "crack_types": [
      {
        "type": "simple",
        "name": "简单密码",
        "description": "6位纯数字密码",
        "max_file_size": 52428800,
        "price": 0.00,
        "estimated_time": 300
      },
      {
        "type": "normal",
        "name": "常规任务",
        "description": "复杂密码",
        "max_file_size": 524288000,
        "price": 29.00,
        "estimated_time": 604800
      },
      {
        "type": "advanced",
        "name": "专业破解",
        "description": "GPU加速",
        "max_file_size": 2147483648,
        "price": 200.00,
        "estimated_time": null
      }
    ],
    "supported_formats": [
      "zip", "rar", "7z", "pdf", "doc", "docx", "xls", "xlsx"
    ],
    "limits": {
      "max_file_size": 2147483648,
      "max_concurrent_tasks": {
        "free": 1,
        "premium": 3,
        "enterprise": 10
      },
      "daily_tasks": {
        "free": 3,
        "premium": 10,
        "enterprise": 100
      }
    },
    "pricing": {
      "memberships": [
        {
          "plan": "premium",
          "name": "高级会员",
          "price": 99.00,
          "duration": 30,
          "discount": 0.9
        },
        {
          "plan": "enterprise",
          "name": "企业会员",
          "price": 999.00,
          "duration": 30,
          "discount": 0.8
        }
      ]
    }
  }
}
```

### 10.2 获取服务状态

**接口**: `GET /health`

**响应**:
```json
{
  "code": 0,
  "data": {
    "status": "healthy",
    "version": "1.0.0",
    "services": {
      "database": "healthy",
      "redis": "healthy",
      "rabbitmq": "healthy",
      "storage": "healthy"
    },
    "queue": {
      "pending_tasks": 100,
      "processing_tasks": 50
    }
  }
}
```

---

**文档版本：1.0**
**创建日期：2024-12-24**
**文档作者：后端架构师**
