# FastAPI + Casbin 多租户/临时授权/数据范围权限方案说明

## 主要核心函数说明

### data_filter_utils.py
```python
# 解析结构化 data_filter JSON 为 SQLAlchemy 查询条件
# 参数: data_filter(JSON字符串), table(SQLAlchemy表), allowed_fields(字段白名单)
def parse_filter(data_filter: str, table=None, allowed_fields=None):
    """将结构化 data_filter JSON 解析为 SQLAlchemy 查询条件，支持字段白名单校验。"""
    ...
```

### casbin_dependency.py
```python
# FastAPI 权限依赖，自动校验并记录审计日志
def casbin_dependency(sub, obj, act, tenant, org="*", data_id="*", data_ctx=None):
    """权限校验依赖，校验通过返回，否则抛出 403。"""
    ...
```

### enforcer.py
```python
# 获取全局单例 Casbin Enforcer
def get_enforcer():
    """返回全局唯一的 Casbin Enforcer 实例，自动加载策略。"""
    ...
```

### audit_log.py
```python
# 记录策略变更和权限校验日志
def log_policy_change(action, policy):
    """记录策略变更日志。"""
    ...
def log_permission_check(user, obj, act, result, detail=None):
    """记录权限校验日志。"""
    ...
```

## 1. 权限模型与表结构
- 采用 Casbin，支持多租户（tenant）、临时授权（expire_at）、数据范围（data_filter）等字段。
- 策略表 casbin_rule 字段：ptype, sub, obj, act, tenant, org, data_id, data_filter, expire_at。
- model.conf 支持多维度匹配与通配符。

### 策略样例
```
p, alice, order, list, tenant1, orgA, *, {"region": "华东", "amount": {">": 10000}}, *
p, bob, order, list, tenant1, orgA, *, {"and": [{"status": "active"}, {"score": {">=": 80}}]}, *
p, alice, order, list, tenant1, orgA, *, *, 2024-12-31T23:59:59
```

### data_filter JSON 示例
- 单条件：`{"region": "华东"}`
- 多条件：`{"and": [{"region": "华东"}, {"amount": {">": 10000}}]}`
- 或条件：`{"or": [{"status": "active"}, {"score": {">=": 80}}]}`

## 2. Enforcer 初始化与依赖注入
- 通过 enforcer.py 的 get_enforcer() 工厂方法，自动加载 model.conf 和数据库策略。
- FastAPI 权限依赖 casbin_dependency，支持多租户、临时授权、数据范围上下文参数。

## 3. 路由集成与数据范围过滤
- 路由中通过 Depends 注入权限校验。
- data_filter 支持表达式，结合 parse_filter 工具转为 SQLAlchemy 查询条件，实现数据范围过滤。

## 4. 临时授权与定时任务
- 策略支持 expire_at 字段，权限依赖和 Celery 定时任务均可自动失效和清理过期策略。

## 5. 日志与审计
- 所有策略变更、权限校验结果通过 audit_log.py 记录到 audit.log，便于合规追溯。

## 6. 部署与运行
1. 安装依赖：`pip install -r requirements.txt`
2. 初始化数据库：执行 casbin_rule.sql
3. 启动 FastAPI 服务：`uvicorn main:app --reload`
4. 启动 Celery 定时任务：`celery -A tasks worker --beat --loglevel=info`

## 7. 扩展建议
- 可开发策略管理后台，支持策略的增删改查、批量导入导出、临时授权、审批等。
- data_filter 建议用更安全的表达式解析库。
- 可扩展更多维度（如环境、时间、IP等），只需扩展 model.conf 和 policy 字段。 